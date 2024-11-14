FROM node:lts-alpine AS ui

WORKDIR /app

COPY ui/ .

RUN npm install
RUN npm run build


FROM python:3.10

WORKDIR /app/zettabgp

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY --from=ui /app/dist/ui/browser/ /app/zettabgp/src/ui/
ENV ZETTABGP_WEBAPP_UI_PATH=/app/zettabgp/src/ui
ENV ZETTABGP_WEBAPP_APP=src.webapp:app
ENV ZETTABGP_WEBAPP_MRT_LIBRARY_PATH=mrt

COPY setup.py .
COPY src/ src/

RUN pip3 install -e .

ENV TZ=Europe/Berlin

WORKDIR /app
