FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git python3 gcc

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]