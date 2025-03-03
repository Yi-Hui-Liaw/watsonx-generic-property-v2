FROM python:3.11-slim

WORKDIR /code/agent

COPY ./agent /code/agent

# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://ollama.com/install.sh | bash

RUN which ollama

RUN pip install -r requirements.txt

RUN crewai install 

CMD ["sh", "-c", "ollama serve & ollama pull llama3 && uvicorn app.main:app --host 0.0.0.0 --port 8080"]