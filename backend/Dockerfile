FROM python:3.11-slim

WORKDIR /code/property_agent

COPY ./property_agent /code/property_agent

COPY ./requirements.txt /code/property_agent/requirements.txt

COPY ./start.sh /code/property_agent/start.sh

# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl sqlite3 libsqlite3-dev gcc && \
    curl -sSL https://ollama.com/install.sh | sh

ENV OLLAMA_HOST=0.0.0.0:11434

RUN pip install --no-cache-dir -r requirements.txt && \
    crewai install

RUN chmod +x /code/property_agent/start.sh

ENTRYPOINT ["/code/property_agent/start.sh"]
