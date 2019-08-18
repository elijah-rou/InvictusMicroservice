FROM python:alpine3.7

RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt ./

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del .build-deps

COPY config.yml ./
COPY src/InvictusService.py ./
COPY src/gutenberg_downloader.py ./

RUN python3 gutenberg_downloader.py
CMD nameko run --config config.yml InvictusService
