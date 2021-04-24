FROM python:3.8-buster

WORKDIR /web-app/

RUN pip install poetry

COPY poetry.lock /web-app/
COPY pyproject.toml /web-app/

RUN poetry install --no-dev

COPY static /web-app/static
COPY templates /web-app/templates

COPY . /web-app/

EXPOSE 8000