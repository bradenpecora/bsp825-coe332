FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install --user redis
RUN pip install --user flask
RUN pip install --user datetime
ENV LC_CTYPE "en_US.UTF-8"
ENV LANG "en_US.UTF-8"
RUN pip install petname==2.6
CMD python app.py