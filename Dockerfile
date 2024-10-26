FROM python:3.10

WORKDIR /app/zettabgp

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY setup.py .
COPY src/ src/

RUN pip3 install -e .

ENV TZ=Europe/Berlin

WORKDIR /app
