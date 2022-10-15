FROM alpine:3.16.0


ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV DB_TYPE=mysql
ENV DB_HOST=atlas_db
ENV DB_USER=marbar
ENV DB_PASSWORD=

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

RUN apk update
RUN apk add build-base python3 python3-dev py3-pip bash py3-mysqlclient
RUN pip3 install -q --no-cache-dir    \
    Pillow                            \
    channels==3.0.5                   \
    channels-redis==3.4.1             \
    django                            \
    django-bootstrap-form             \
    ipython                           \
    mysqlclient                       \
    tzdata

ADD ./stregsystem/ /usr/share/www/
WORKDIR /usr/share/www

COPY ./runserver.sh /usr/bin
RUN [ "chmod", "+x", "/usr/bin/runserver.sh" ]

EXPOSE 8000:8000

ENTRYPOINT [ "runserver.sh" ]
