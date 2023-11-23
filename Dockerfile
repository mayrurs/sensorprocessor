FROM python:3.11.6-slim-bookworm

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src/
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src

