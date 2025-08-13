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

def connect_es():
    es_url = "http://itzvsi-693000gwtq-wxd-1xy2tsbq.techzone.ibm.com:9200/"
    es = Elasticsearch(hosts=es_url, basic_auth=ES_CREDENTIALS, verify_certs=False, ssl_show_warn=False, request_timeout=600)
    print(es.info())
    return es

def es_query(es, index_name, question, model_name):
    res = es.search(
        index=index_name,
        body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "sparse_vector": {
                                "field": "text_embedding",
                                "inference_id": model_name,
                                "query": question
                            }
                        }
                    ],
                    "must_not": [
                        { "term": { "status.keyword": "Sold Out" } },
                        { "term": { "status.keyword": "Coming Soon" } }
                    ]
                }
            },
            "size": 5
        },
    )
    print(res.body['hits']['hits'][0]['_source']['page_content'])

    
if __name__ == "__main__":
    INDEX_NAME = "property_data"
    #SPACE_ID = "ba377fa4-6bce-4ec2-b0b2-911bb9d26238"
    PIPELINE_ID = "ingest-pipeline-property"
    WML_CREDENTIALS = {"apikey": os.getenv("WATSONX_API_KEY"), "url": "https://us-south.ml.cloud.ibm.com"}
    ES_CREDENTIALS = (os.getenv("ES_USERNAME"), os.getenv("ES_PASSWORD"))
    model_name = ".elser_model_2"

    es = connect_es()
    es_query(es, INDEX_NAME, "Properties in Mont Kiara with price 500k", model_name)