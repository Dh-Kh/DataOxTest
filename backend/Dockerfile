FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

COPY requirements.txt /backend
RUN pip install -r requirements.txt 

COPY . /backend
