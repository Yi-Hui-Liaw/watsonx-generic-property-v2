FROM python:3.11-slim

WORKDIR /code/property_agent

COPY ./property_agent /code/property_agent

COPY ./ollama.sh /code/property_agent/ollama.sh

COPY ./requirements.txt /code/property_agent/requirements.txt

# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl sqlite3 libsqlite3-dev gcc && \
    curl -sSL https://ollama.com/install.sh | sh

ENV OLLAMA_HOST=0.0.0.0:11434

RUN ./ollama.sh

RUN pip install --no-cache-dir -r requirements.txt && \
    crewai install

# CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080"]
CMD ["uvicorn app.main:app --host 0.0.0.0 --port 8080"]