FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y wget gnupg2 \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
    
RUN apt-get update \
    && apt-get install -y postgresql-client-16=16.1-1.pgdg120+1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

COPY requirements.txt /backend
RUN pip install -r requirements.txt 

COPY . /backend
EXPOSE 8000