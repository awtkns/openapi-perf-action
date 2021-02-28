FROM python

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./openapi-perf-app /src
CMD python /src/main.py
