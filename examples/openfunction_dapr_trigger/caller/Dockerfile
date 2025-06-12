FROM python:3.12.11-slim

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY *.py /app/

CMD [ "python", "main.py" ]