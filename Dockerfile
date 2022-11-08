FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip3 install -r requirements.txt
RUN /bin/sh -c python manage.py makemigrations blog
RUN /bin/sh -c python manage.py sqlmigrate blog 0001
RUN /bin/sh -c python manage.py migrate;
RUN apt-get update && apt-get install iputils-ping -y

COPY . /code/
