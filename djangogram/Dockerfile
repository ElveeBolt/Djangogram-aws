FROM python:3.10-alpine

WORKDIR /mnt/data/djangogram

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY entrypoint.sh .

RUN chmod +x /mnt/data/djangogram/entrypoint.sh

ENTRYPOINT ["/mnt/data/djangogram/entrypoint.sh"]