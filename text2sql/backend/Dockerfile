FROM python:3.11-slim

# RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN mkdir /code/db

COPY ./app /code/app

COPY ./vdb /code/vdb

COPY ./data /code/data

COPY ./static /code/static

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
