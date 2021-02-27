FROM python:alpine


COPY main.py /src/main.py
CMD python /src/main.py
