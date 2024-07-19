FROM python:3.11-slim-buster

WORKDIR /app

RUN apt update

RUN pip3 install --upgrade pip

RUN pip3 install nestipy-cli nestipy

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

CMD ["nestipy", "start", "--dev"]