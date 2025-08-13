FROM python:3.11-slim
WORKDIR /code/property_agent

# Install system dependencies needed for your app & building packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gcc libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./property_agent /code/property_agent
COPY ./requirements.txt /code/property_agent/requirements.txt
COPY ./start.sh /code/property_agent/start.sh

EXPOSE 8080

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    crewai install

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
