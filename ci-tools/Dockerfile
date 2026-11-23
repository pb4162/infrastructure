FROM python:3.15.2-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

RUN apt update && apt install -y git && apt clean

WORKDIR /scripts

COPY scripts .
