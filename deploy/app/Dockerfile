FROM python:3

ADD app/ /app
WORKDIR /app
COPY /app/requirements.txt /tmp/requirements.txt

RUN apt-get install default-libmysqlclient-dev

RUN pip install --no-cache-dir -r /tmp/requirements.txt