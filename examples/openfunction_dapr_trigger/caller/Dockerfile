FROM python:3.14.0-slim

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY *.py /app/

CMD [ "python", "main.py" ]