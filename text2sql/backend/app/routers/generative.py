import re

import pandas as pd
from fastapi import APIRouter, Depends, Request
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from langchain.vectorstores import FAISS
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..action import ACTIONS
from ..database import get_db
from ..llm import EMBEDDING, MODEL
from ..prompt import (
    DEFAULT_SYSTEM_PROMPT,
    DIRECT_ANSWER_TEMPLATE,
    QUESTION_TEMPLATE,
    ROUTING_TEMPLATE,
    PROPERTY_TEMPLATE,
    SQL_SYSTEM_PROMPT,
    SQL_TEMPLATE,
    build_prompt,
)
from ..utils import GenerateRequest, GenerateResponse

vdb = FAISS.load_local("vdb", EMBEDDING, allow_dangerous_deserialization=True)
router = APIRouter()

params = {
    "model": MODEL,
    "vdb": vdb,
    "property": None,
}


@router.post("/api/generate")
def generate(
    request: Request, generate_request: GenerateRequest, db: Session = Depends(get_db)
) -> GenerateResponse:
    k_docs = generate_request.k_docs
    wa_property = generate_request.current_page
    messages = generate_request.history
    question = messages[-1]["u"]
    prompt = ROUTING_TEMPLATE.replace("{{question}}", question)
    #(1) Call LLM to route
    action_output = int(params['model'](prompt).strip())
    if action_output in [1, 3]:
        property = None
        #(2) Call LLM to get property name
        property_name = params['model'](
            PROPERTY_TEMPLATE.replace("{{question}}", question)
        ).strip()
        if wa_property is not None:
            property = wa_property
        if property_name != "NONE":
            property = property_name
        params.update(
            {
                "question": question,
                "property": property,
                "detected_property_name": property_name
            }
        )
    else:
        params.update({"question": question, "property": None, "detected_property_name": "NONE"})

    params.update({"db": db})
    print(f"Question: {question} - [Action: {action_output}]")
    #(3) Call LLM to get property name
    generated_text, custom_response = ACTIONS[action_output](params).values()
    return {"generated_text": generated_text, "custom_response": custom_response}
