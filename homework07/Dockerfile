FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./source /app
WORKDIR /app

ENTRYPOINT [ "python" ]