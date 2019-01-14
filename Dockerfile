FROM python:3.7.2-alpine

WORKDIR /opt/bamboo

COPY requirements.txt requirements.txt
COPY config.py config.py
COPY create_superuser.py create_superuser.py
COPY init_db.py init_db.py
COPY bamboo bamboo

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev bash
RUN pip3 install -r requirements.txt

EXPOSE 5000