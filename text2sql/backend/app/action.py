import re
import json
import pandas as pd
from sqlalchemy import text
from .prompt import (
    build_prompt,
    SQL_TEMPLATE,
    QUESTION_TEMPLATE,
    DIRECT_ANSWER_TEMPLATE_v1,
    DIRECT_ANSWER_TEMPLATE_v2,
    CUSTOM_RESPONSE_TEMPLATE,
    SQL_SYSTEM_PROMPT,
    DEFAULT_SYSTEM_PROMPT,
    build_prompt_llama3
)
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from typing import TypedDict, Any
from sqlalchemy.orm import Session

IMAGES = [
    "the-nexus-one/pool-lounge.jpg",
    "the-nexus-one/gym.jpg",
    "the-nexus-one/play-area.jpg",
    "the-nexus-one/aerial-night.jpg",
    "the-nexus-one/drop-off.jpg",
    "the-nexus-one/lobby.jpg",
    "the-nexus-one/mid-balcony.jpg",
    "the-nexus-one/mrt-night.jpg",
    "the-nexus-one/parcel-room.jpg",
    "the-nexus-one/pool-top.jpg",
    "the-nexus-one/retail-cafe.jpg",
    "the-lumenh/drop-off.jpg",
    "the-lumenh/garden.jpg",
    "the-lumenh/gym.jpg",
    "the-lumenh/play-area-indoor.jpg",
    "the-lumenh/play-area-outdoor.jpg",
    "abc-residence/gamers-room.jpg",
    "abc-residence/gym.jpg",
    "abc-residence/parcel-lounge.jpg",
    "abc-residence/play-area.jpg",
    "abc-residence/pool-1.jpg",
    "abc-residence/pool-2.jpg",
]

# reference_urls1 = {
#     "minh":"The MINH URL",
#     "zig":"Residensi Zig URL",
#     "connaught":"The Connaught One URL",
# }

# reference_urls2 = {
#     "The MINH URL":"https://www.uemsunrise.com/property/region/greater-kuala-lumpur/project/the-lumenh",
#     "Residensi Zig URL":"https://www.uemsunrise.com/property/region/greater-kuala-lumpur/project/abc-residence",
#     "The Connaught One URL":"https://www.uemsunrise.com/property/region/greater-kuala-lumpur/project/the-nexus-one",
# }

class ActionParams(TypedDict):
    question: str
    models: list
    db: Session
    vdb: Any
    property: str

def postprocess_numeric(text):
    text = re.sub("([0-9]+)\.0", r"\1", text)
    text = re.sub("(^|\D)([0-9])([0-9][0-9][0-9])($|\D)", r"\1\2,\3\4", text)
    text = re.sub("(^|\D)([0-9][0-9])([0-9][0-9][0-9])($|\D)", r"\1\2,\3\4", text)
    text = re.sub("(^|\D)([0-9][0-9][0-9])([0-9][0-9][0-9])($|\D)", r"\1\2,\3\4", text)
    text = re.sub("(^|\D)([0-9])([0-9][0-9][0-9])([0-9][0-9][0-9])($|\D)", r"\1\2,\3,\4\5", text)
    return text


def transactional_query(params: ActionParams):
    question = params["question"]
    model = params["model"]
    db = params["db"]
    # if params["property"] is None:
    #     return {
    #         "generated_text": "Sounds like you're asking a question about a property. Kindly specify a valid property name so that I can answer this question correctly.",
    #         "custom_response": {},
    #     }
    if params["property"] is not None and params["detected_property_name"] == "NONE":
        prop_replace = params["property"]
        question = f"For {prop_replace}, {question}"
    prompt = build_prompt(
        SQL_TEMPLATE.replace("{{question}}", question), SQL_SYSTEM_PROMPT
    )
    sql = model(prompt).strip()
    if "```" in sql:
        sql = re.search("```\n([\S\s]*);\n", sql).group(1)
    if "UNION" in sql:
        sql = re.sub("\n", " ", sql)
        sql = re.sub("SELECT ([a-zA-z\(\*\)]+) FROM ([a-zA-z]+)", r"SELECT \1, '\2' as property_name FROM \2", sql.strip())
        print(f"Generated SQL Query: {sql}")
        with db.connection().engine.connect() as conn:
            results = pd.read_sql(text(sql), conn)
            # for rn in results.columns:
            #     if "Price" in rn:
            #         results.loc[:, rn] = results[rn].map('{:,.0f}'.format)
        ordered_tb_names = results["property_name"][:5]
        # results = results.drop(columns=["property_name"])
    else:
        print(f"Generated SQL Query: {sql}")
        with db.connection().engine.connect() as conn:
            results = pd.read_sql(text(sql), conn)
            # for rn in results.columns:
            #     if "Price" in rn:
            #         results.loc[:, rn] = results[rn].map('{:,.0f}'.format)
        ordered_tb_names = None
    if results.shape == (1, 1):
        answer = str(results.iloc[0, 0])
        prompt = DIRECT_ANSWER_TEMPLATE_v1.replace("{{answer}}", answer).replace(
            "{{question}}", question
        )
        generated_text = model(prompt).strip()
    elif results.shape[1] <= 2:
        generated_text = results.head(5).to_json(orient="records")
        if "UNION" in sql:
            if len(set(list(results["property_name"])))==3 and results.shape[0]==3:
                queried = ", ".join(ordered_tb_names)
                generated_text += f"\nInfo provided is for the following properties: {queried}"
                prompt = DIRECT_ANSWER_TEMPLATE_v2.replace("{{answer}}", generated_text).replace(
                "{{question}}", question
            )
                generated_text = model(prompt).strip()
            else:
                generated_text = "Here are some relevant results that we found: \n" + generated_text
        else:
            prompt = DIRECT_ANSWER_TEMPLATE_v2.replace("{{answer}}", generated_text).replace(
                "{{question}}", question
            )
            generated_text = model(prompt).strip()
        if results.shape[0]>5:
            table = re.findall("FROM ([a-z]+)", sql)
            table = ", ".join([reference_urls1[t] for t in table])
            generated_text += f"\nPlease note that there are more than 5 relevant results. Please refer to {table} for more information"

    elif results.shape[0] == 1:
        results = results.transpose()
        generated_text = results.head(5).to_json(orient="records")
        if "UNION" in sql:
            if len(set(list(results["property_name"])))==3 and results.shape[0]==3:
                queried = ", ".join(ordered_tb_names)
                generated_text += f"\nInfo provided is for the following properties: {queried}"
                prompt = DIRECT_ANSWER_TEMPLATE_v2.replace("{{answer}}", generated_text).replace(
                "{{question}}", question
            )
                generated_text = model(prompt).strip()
            else:
                generated_text = "Here are some relevant results that we found: \n" + generated_text
        else:
            prompt = DIRECT_ANSWER_TEMPLATE_v2.replace("{{answer}}", generated_text).replace(
                "{{question}}", question
            )
            generated_text = model(prompt).strip()
        if results.shape[0]>5:
            table = re.findall("FROM ([a-z]+)", sql)
            # table = ", ".join([reference_urls1[t] for t in table])
            generated_text += f"\nPlease note that there are more than 5 relevant results. Please refer to {table} for more information"

    else:
        print(results)
        generated_text = "Sorry, that type of query is not currently supported - you need to be more specific"

    generated_text = generated_text.replace("abc-residence", "ABC Residence")
    generated_text = generated_text.replace("the-nexus-one", "The Nexus One")
    generated_text = generated_text.replace("the-lumenh", "The LUMENH")
    generated_text = generated_text.replace("abc", "ABC Residence")
    generated_text = generated_text.replace("connaught", "The Nexus One")
    generated_text = generated_text.replace("lumenh", "The LUMENH")

    # for x in reference_urls2:
    #     generated_text = generated_text.replace(x, reference_urls2[x])

    generated_text = postprocess_numeric(generated_text)
    return {"generated_text": generated_text, "custom_response": {}}



# def general_transactional_query(params: ActionParams):
#     question = params["question"]
#     models = params["models"]
#     db = params["db"]
#     prompt = build_prompt(
#         SQL_TEMPLATE.replace("{{question}}", question), SQL_SYSTEM_PROMPT
#     )
#     sql = models[ModelTypes.LLAMA_2_70B_CHAT](prompt).strip()
#     if "```" in sql:
#         sql = re.search("```\n([\S\s]*);\n", sql).group(1)
#     if "UNION" in sql:
#         sql = re.sub("\n", " ", sql)
#         sql = re.sub(
#             "SELECT ([a-zA-z\(\*\)]+) FROM ([a-zA-z]+)",
#             r"SELECT \1, '\2' as tablename FROM \2",
#             sql.strip(),
#         )
#         print(f"Generated SQL Query: {sql}")
#         with db.connection().engine.connect() as conn:
#             results = pd.read_sql(text(sql), conn)
#         ordered_tb_names = results["tablename"]
#         results = results.drop(columns=["tablename"])
#     else:
#         print(f"Generated SQL Query: {sql}")
#         with db.connection().engine.connect() as conn:
#             results = pd.read_sql(text(sql), conn)
#         ordered_tb_names = None
#     if results.shape[1] == 1:
#         generated_text = "\n".join(
#             [str(x) for x in pd.Series(results.iloc[:, 0].head(5)).tolist()]
#         )
#         if (
#             "UNION" in sql
#             and ordered_tb_names is not None
#             and len(ordered_tb_names) == 3
#         ):
#             queried = ", ".join(ordered_tb_names)
#             generated_text += (
#                 f"\nInfo provided is for the following properties: {queried}"
#             )
#         if results.shape[0] > 5:
#             table = ", ".join(re.findall("FROM ([a-z]+)", sql))
#             generated_text += f"\nPlease note that there are more than 5 relevant results. Please refer to {table} table for more information"
#     elif results.shape[0] == 1:
#         results_t = results.transpose()
#         generated_text = "\n".join(
#             [str(x) for x in pd.Series(results_t.iloc[:, 0].head(5)).tolist()]
#         )
#         if (
#             "UNION" in sql
#             and ordered_tb_names is not None
#             and len(ordered_tb_names) == 3
#         ):
#             queried = ", ".join(ordered_tb_names)
#             generated_text += (
#                 f"\nInfo provided is for the following properties: {queried}"
#             )
#         if results_t.shape[0] > 5:
#             table = ", ".join(re.findall("FROM ([a-z]+)", sql))
#             generated_text += f"\nPlease note that there are more than 5 relevant results. Please refer to {table} table for more information"
#     else:
#         generated_text = "Sorry, that type of query is not currently supported - you need to be more specific"

#     return {"generated_text": generated_text, "custom_response": {}}


def property_specific_general_query(params: ActionParams):
    question = params["question"]
    models = params["models"]
    vdb = params["vdb"]
    property = params["property"]
    if params["property"] is None:
        return {
            "generated_text": "Sounds like you're asking a question about a property. Kindly specify a valid property name so that I can answer this question correctly.",
            "custom_response": {},
        }
    search_results = vdb.similarity_search(question, k=3)
    if property:
        print(f"Property: {property}")
        search_results = list(
            filter(lambda x: x.metadata["filename"] == property, search_results)
        )
    context = " ".join([x.page_content for x in search_results])
    print("context", context)
    print(len(search_results))
    prompt = build_prompt(
        QUESTION_TEMPLATE.replace("{{context}}", context).replace(
            "{{question}}", question
        ),
        DEFAULT_SYSTEM_PROMPT,
    )
    generated_text = models[ModelTypes.LLAMA_2_70B_CHAT](prompt).strip()
    prompt = build_prompt_llama3([{"u":CUSTOM_RESPONSE_TEMPLATE.replace("{{description}}", generated_text)}], DEFAULT_SYSTEM_PROMPT, "", "")
    custom_response = {}
    generated_custom_response = models["meta-llama/llama-3-70b-instruct"](prompt).strip()
    print("check imgs", generated_custom_response)
    if "None" not in generated_custom_response:
        try:
            custom_response["images"] = json.loads(
                generated_custom_response.replace("'", '"')
            )
            custom_response["images"] = [
                x for x in custom_response["images"] if x in IMAGES
            ]
        except Exception:
            pass

    return {"generated_text": generated_text, "custom_response": custom_response}


def general_query(params: ActionParams):
    generated_text = (
        "We do not have the answer right now. Please check back at a later time."
    )
    return {"generated_text": generated_text, "custom_response": {}}

# General query is build from conversational search
ACTIONS = {
    1: transactional_query,
    # 2: general_transactional_query,
    # 3: property_specific_general_query,
    4: general_query,
}
