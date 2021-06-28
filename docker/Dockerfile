FROM python:3.8-slim-buster

# Install dependencies:
COPY requirements.txt .
RUN  apt-get update && pip install -r requirements.txt

COPY . .

# docker run --rm --env-file=prodcredentials -v ~/credentials.json:~/credentials.json uotmakhova/product-metrics python -m product_metrics.core