FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip && \
    pip install "poetry"

RUN poetry config virtualenvs.create false

WORKDIR /src

COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN poetry install --no-root

COPY . .

