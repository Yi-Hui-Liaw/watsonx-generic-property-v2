FROM python:3.11-slim

WORKDIR /code/property_agent

COPY ./property_agent /code/property_agent

COPY ./requirements.txt /code/property_agent/requirements.txt

# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN apt-get update && apt-get -y install --no-install-recommends \
    curl sqlite3 libsqlite3-dev gcc && \
    curl -sSL https://ollama.com/install.sh | bash

ENV OLLAMA_HOST=localhost:11434

RUN which ollama

# RUN systemctl enable ollama && systemctl start ollama

RUN pip install -r requirements.txt

RUN crewai install 

CMD ["sh", "-c", "ollama serve & ollama pull llama3 && uvicorn app.main:app --host 0.0.0.0 --port 8080"]