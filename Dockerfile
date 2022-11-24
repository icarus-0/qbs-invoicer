FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /qbs_invoicer

ADD . /qbs_invoicer

COPY ./requirements.txt /qbs_invoicer/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt



