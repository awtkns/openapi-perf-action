FROM python:alpine
WORKDIR /src

ENV PYTHONPATH /src

COPY main.py main.py

CMD python main.py