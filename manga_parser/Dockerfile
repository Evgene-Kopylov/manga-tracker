FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


WORKDIR /manga_parser

COPY . /manga_parser
RUN pip install -r requirements.txt

CMD python insta_ckeck.py
