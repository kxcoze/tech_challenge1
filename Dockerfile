FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PUTHONBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
