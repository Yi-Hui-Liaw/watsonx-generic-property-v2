from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .utils import AgentRequest, AgentResponse
from src.healthcare.flows.flow import RouterFlow
import pandas as pd

router = APIRouter()


LIMIT_WINDOW = 15 

# Front end hosted seperately as nodejs + vue
# @router.get("/")
# async def page_home():
#     return FileResponse('static/home.html')

# @router.get("/main")
# async def page_main():
#     return FileResponse('static/main.html')

@router.get("/csv/appointment", response_class=HTMLResponse)
async def read_patient():
    df = pd.read_csv("knowledge/csv/appointment.csv")
    return df.to_html()

@router.get("/csv/minh", response_class=HTMLResponse)
async def read_patient():
    df = pd.read_csv("knowledge/csv/minh.csv")
    return df.to_html()

@router.get("/csv/zig", response_class=HTMLResponse)
async def read_patient():
    df = pd.read_csv("knowledge/csv/zig.csv")
    return df.to_html()

@router.get("/csv/connaught", response_class=HTMLResponse)
async def read_patient():
    df = pd.read_csv("knowledge/csv/connaught.csv")
    return df.to_html()

@router.get("/csv/refresh")
async def read_patient():
    try:
        appt = pd.read_csv("knowledge/csv_archive/appointment.csv")
        appt.to_csv("knowledge/csv/appointment.csv", index=False)

        return "CSV refreshed succcessfully"
    except Exception as e:
        return f"Refresh failed {e}"

@router.post("/api/agent_flow")
def flow(request: AgentRequest) -> AgentResponse:
    history = request.history[:LIMIT_WINDOW]

    flow = RouterFlow()
    result = flow.kickoff(inputs={"inputs": history})
    
    return {"response":result}