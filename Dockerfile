FROM alpine:3.16.0

RUN apt-get install -y python3 py3-pip
RUN pip3 install -q --no-cache-dir django django-bootstrap-form Pillow channels

VOLUME ["stregsystem"]

EXPOSE 8000:8000
