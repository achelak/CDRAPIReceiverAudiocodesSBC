FROM python:3.8.2-alpine

COPY ./requirements.txt /opt/cdr_api/requirements.txt

WORKDIR /opt/cdr_api

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /opt/cdr_api

RUN ["chmod", "+x", "/opt/cdr_api/gunicorn_starter.sh"]

ENTRYPOINT ["./gunicorn_starter.sh"]

