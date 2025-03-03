from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from .base import router

import logging

logging.basicConfig(level=logging.INFO)


app = FastAPI(docs_url=None, redoc_url=None, openapi_url = None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/openapi.json")
async def openapi(request: Request):
    # This func is to compensate wx assistant only support swagger < 3.0.3
    openapi =  get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)
    url = request.base_url._url[:-1]
    openapi["openapi"] = "3.0.3"
    openapi["info"] = {
        "title": "watsonx.ai generation API endpoint",
        "version": "0.1.0",
    }
    openapi["servers"] = [{"url": url, "description": "watsonx.ai endpoint"}]
    
    # TODO: Update to remove anyof func, not support by wxAsssistant
    # if "components" in openapi:
        # del openapi["components"]["schemas"]["HTTPValidationError"]
        # del openapi["components"]["schemas"]["ValidationError"]
    for k in openapi["paths"].keys():
        if "post" in openapi["paths"][k]:
            del openapi["paths"][k]["post"]["responses"]["422"]
    return openapi

@app.get("/docs")
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

# app.add_api_route("/openapi", endpoint=openapi_update)
app.include_router(router)