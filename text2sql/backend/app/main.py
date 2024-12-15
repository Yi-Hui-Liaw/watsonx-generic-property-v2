import secrets
from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles
from langchain.vectorstores import FAISS

from .utils import openapi
from .routers import base, generative

router = APIRouter()
security = HTTPBasic()


# https://github.com/tiangolo/fastapi/issues/858
async def auth(request: Request):
    credentials = await security(request)
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "watsonx")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    # return credentials.username


class AuthStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:
        assert scope["type"] == "http"
        request = Request(scope, receive)
        await auth(request)
        await super().__call__(scope, receive, send)


# app = FastAPI(dependencies=[Depends(auth)])
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_api_route("/openapi", endpoint=openapi)
app.include_router(base.router)
app.include_router(generative.router)

# app.mount("/", AuthStaticFiles(directory="static", html=True), name="static")
# app.mount("/", StaticFiles(directory="static", html=True), name="static")
