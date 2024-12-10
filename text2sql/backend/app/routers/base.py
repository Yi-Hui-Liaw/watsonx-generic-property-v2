import io
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import APIRouter, Depends
from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from fastapi import APIRouter, Request
import requests
import os 

from ..database import engine, get_db


router = APIRouter()



router = APIRouter()


@router.get("/the-nexus-one")
async def nexus():
    return FileResponse("static/the-nexus-one.html")


@router.get("/the-lumenh")
async def lumenh():
    return FileResponse("static/the-lumenh.html")


@router.get("/abc-residence")
async def abc():
    return FileResponse("static/abc-residence.html")

@router.get("/settings")
async def settings():
    return FileResponse("static/settings.html")


@router.get("/api/hello")
def hello():
    return {"hello": "world"}


@router.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    data = []
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), sheet_name=None)
        for k, v in df.items():
            v.columns = [x.replace(" ", "_") for x in v.columns]
            table = k.split(" ")[0]
            v.to_sql(table, con=engine, index=False, if_exists="replace")
        # data = df.head().to_dict(orient="records")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )
    finally:
        await file.close()
    return {"data": data}


@router.get("/api/database")
def database(db: Session = Depends(get_db)):
    data = []
    with db.connection().engine.connect() as conn:
        df = pd.read_sql(
            text("SELECT name FROM sqlite_master WHERE type='table'"), conn
        )
        for name in df["name"]:
            table = pd.read_sql(text(f"SELECT * from {name} LIMIT 5"), conn)
            table["id"] = table.index
            data.append(
                {
                    "name": name,
                    "data": table.to_dict(orient="records"),
                }
            )
    return data

def openapi_update(request: Request):
    url = request.base_url._url[:-1]
    openapi = requests.get(f"{url}/openapi.json", auth=(os.getenv("FASTAPI_USERNAME"), os.getenv("FASTAPI_PASSWORD"))).json()
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
        openapi["components"]["securitySchemes"] = {"basicAuth": {"type": "http", "scheme": "basic"}}
    for k in openapi["paths"].keys():
        if "post" in openapi["paths"][k]:
            del openapi["paths"][k]["post"]["responses"]["422"]
    return openapi
