from typing import Any, Mapping, List

import requests
from fastapi import Request
from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    documents: List[str] = None
    length: str = "short"


class GenerateResponse(BaseModel):
    generated_text: str
    custom_response: dict


class GenerateRequest(BaseModel):
    k_docs: int = 3
    model_name: str = "meta-llama/llama-2-70b-chat"
    current_page: str = None
    history: List[Mapping[str, Any]] = None


def openapi(request: Request):
    url = request.base_url._url[:-1]
    openapi = requests.get(f"{url}/openapi.json").json()
    openapi["openapi"] = "3.0.3"
    openapi["info"] = {
        "title": "watsonx.ai generation API endpoint",
        "version": "0.1.0",
    }
    openapi["servers"] = [{"url": url, "description": "watsonx.ai endpoint"}]
    # if "paths" in openapi:
    #     del openapi["paths"]["/"]
    if "/openapi" in openapi["paths"]:
        del openapi["paths"]["/openapi"]
    for x in [x for x in openapi["paths"] if not x.startswith("/api")]:
        del openapi["paths"][x]
    if "components" in openapi:
        del openapi["components"]["schemas"]["HTTPValidationError"]
        del openapi["components"]["schemas"]["ValidationError"]
    for k in openapi["paths"].keys():
        if "post" in openapi["paths"][k]:
            del openapi["paths"][k]["post"]["responses"]["422"]
    return openapi
