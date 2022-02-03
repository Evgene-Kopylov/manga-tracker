FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


WORKDIR /web_app

COPY . /web_app
RUN pip install -r requirements.txt

CMD python main.py
