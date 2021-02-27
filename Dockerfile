FROM python:alpine

COPY main.py main.py

ENTRYPOINT ['python main.py']