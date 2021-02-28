FROM python

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./action /src
CMD python /src/main.py
