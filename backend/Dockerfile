FROM python:3.11-slim

WORKDIR /code/property_agent

COPY ./property_agent /code/property_agent

COPY ./requirements.txt /code/property_agent/requirements.txt

# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN apt-get update && apt-get install -y --no-install-recommends curl sqlite3 libsqlite3-dev gcc && \
    curl -sSL https://ollama.com/install.sh | sh

ENV OLLAMA_HOST=0.0.0.0:11434

RUN which ollama 

# RUN systemctl enable ollama && systemctl start ollama
RUN ollama serve & sleep 5 && ollama pull llama3 && \
    pip install --no-cache-dir -r requirements.txt

RUN crewai install 

# CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080"]
CMD ["uvicorn app.main:app --host 0.0.0.0 --port 8080"]