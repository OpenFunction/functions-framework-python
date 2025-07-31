FROM python:3.14.0rc1-slim

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY *.py /app/

CMD [ "python", "main.py" ]