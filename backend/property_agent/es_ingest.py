import os
import time
from datetime import datetime, timedelta

from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.prompts import PromptTemplate, PromptTemplateManager
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from llama_index.core.node_parser import SentenceSplitter
import json
from elasticsearch.helpers import BulkIndexError
load_dotenv(override=True)

def connect_es(es_url, es_credentials):
    es_url = os.getenv()
    es = Elasticsearch(hosts=es_url, basic_auth=es_credentials, verify_certs=False, ssl_show_warn=False, request_timeout=600)
    print(es.info())
    return es

def create_hybrid_pipeline(pipeline_id, es):
    # client.ingest.put_pipeline(
    #     id=ingest_pipeline_id,
    #     description="Ingest pipeline for WatsonX vector format",
    #     processors=[
    #         {
    #             "inference": {
    #                 "model_id": ".elser_model_2",
    #                 "input_output": {
    #                     "input_field": "web_text",
    #                     "output_field": "vector.tokens"
    #                 }
    #             }
    #         },
    #         {
    #             "set": {
    #                 "field": "vector.model_id",
    #                 "value": ".elser_model_2"
    #             }
    #         }
    #     ]
    # )
    pipeline_body = {
        "processors": [
            {
                "inference": {
                    "model_id": model_name,
                    "input_output": {"input_field": "page_content", "output_field": "text_embedding"},
                }
            }
        ],
    }
    
    #es.ingest.delete_pipeline(id=pipeline_id)
    
    es.ingest.put_pipeline(id=pipeline_id, body=pipeline_body)


def create_hybrid_index(index_name, pipeline_id, es):
    if es.indices.exists(index=index_name):
        print("Index exists!!! Index is NOT created. Using the existing index ", index_name)
        return
    # Create a new index
    # client.indices.delete(index=index_name, ignore_unavailable=True)
    es.indices.create(
        index=INDEX_NAME,
        settings={"index": {"default_pipeline": pipeline_id}},
        mappings={
            "properties": {
                "page_content": {"type": "text"},
                "text_embedding": {"type": "sparse_vector"}
            }
        },
    )

def ingest_bulk(es, documents_gen, chunk_size=200):
    try:
        helpers.bulk(es, documents_gen, chunk_size)
    except BulkIndexError as e:
        with open("err.txt", "a+") as f:
            f.write(str(e.errors))
        # print("Bulk index error:", e)
        # for error in e.errors:
        #     print(error)

def preprocess_data(folder_path):
    ingestion_timestamp = datetime.now().strftime('%Y%m%d')
    splitter = SentenceSplitter(chunk_size=2000, chunk_overlap=200)

    all_data = []

    # Load and prepare data
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    for entry in data:
                        entry['file_name'] = filename
                        entry['last_update'] = ingestion_timestamp
                    data = {"data": data}
                else:
                    data['file_name'] = filename
                    data['last_update'] = ingestion_timestamp
                all_data.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {filename}: {e}")

    # Helper to format JSON to markdown
    def format_to_md(json_dict):
        def format_value(v):
            if isinstance(v, dict):
                return "\n".join(f"- **{k}**: {format_value(val)}" for k, val in v.items())
            elif isinstance(v, list):
                return "\n".join(f"- {format_value(item)}" for item in v)
            else:
                return str(v)

        md_str = ""
        for k, v in json_dict.items():
            if k not in ["page_title", "page_url", "file_name", "last_update", "content"]:
                md_str += f"{' '.join(k.split('_')).title()}\n--\n{format_value(v)}\n--\n\n"
        return md_str

    # Helper to chunk document with metadata
    def chunk_doc(json_dict):
        chunks = splitter.split_text(json_dict["page_content"])
        if not chunks:
            chunks = [""]
        chunked_dicts = [{k: v for k, v in json_dict.items() if k != "page_content"} for _ in chunks]
        for chunk_dict, chunk_text in zip(chunked_dicts, chunks):
            for field in ["page_title", "page_url", "file_name"]:
                if field in chunk_dict:
                    chunk_text = f"{field.title()}\n---\n{chunk_dict[field]}\n---\n" + chunk_text
            chunk_dict["page_content"] = chunk_text
        return chunked_dicts

    new_all_data = []
    for entry in all_data:
        entries_list = entry.get("data", [entry])
        for item in entries_list:
            item["page_title"] = item.get("property_name", "")
            item["page_url"] = item.get("url", "")
            item["page_content"] = format_to_md(item)
            if "content" in item:
                del item["content"]
            new_all_data.extend(chunk_doc(item))
    return new_all_data

def gen_processed(new_all_data):
    for e, x in enumerate(new_all_data):
        print(e)
        yield {
            "_op_type": "index",
            "_index": INDEX_NAME,
            "_source": x,
            "pipeline": PIPELINE_ID
        }

    
if __name__ == "__main__":
    INDEX_NAME = "property_data"
    #SPACE_ID = "ba377fa4-6bce-4ec2-b0b2-911bb9d26238"
    PIPELINE_ID = "ingest-pipeline-property"
    WML_CREDENTIALS = {"apikey": os.getenv("WATSONX_API_KEY"), "url": "https://us-south.ml.cloud.ibm.com"}
    ES_CREDENTIALS = (os.getenv("ES_USERNAME"), os.getenv("ES_PASSWORD"))
    ES_URL = os.getenv("ES_URL")
    model_name = ".elser_model_2"

    es = connect_es(ES_URL, ES_CREDENTIALS)
    #create_hybrid_pipeline(PIPELINE_ID, es)
    #create_hybrid_index(INDEX_NAME, PIPELINE_ID, es)
    
    chunks_folder = './property_json'
    # file_names = os.listdir(chunks_folder)

    # t_start_all = time.time()
    all_chunks = preprocess_data(chunks_folder)
    ingest_bulk(es, gen_processed(all_chunks), chunk_size=200)
    # print(f"Total Ingestion time: {time.time() - t_start_all}" )