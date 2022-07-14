FROM alpine:3.16.0

RUN apt-get python3 py3-pip
RUN pip3 install django
