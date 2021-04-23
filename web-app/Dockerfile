FROM python:3.8-buster

WORKDIR /web-app/

RUN pip install poetry

COPY poetry.lock /web-app/
COPY pyproject.toml /web-app/

COPY static /web-app/static
COPY templates /web-app/templates

RUN poetry install

COPY . /web-app/

CMD ["poetry", "run", "alembic", "upgrade", "head"]
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]