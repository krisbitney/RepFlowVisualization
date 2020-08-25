FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git python3 gcc

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

RUN python server.py

EXPOSE 5000

CMD ["python", "/server.py"]