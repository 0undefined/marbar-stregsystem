FROM alpine:3.16.0

WORKDIR /usr/share/www

ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV DB_TYPE=MYSQL
ENV DB_HOST=atlas_db
ENV DB_USER=marbar
ENV DB_PASSWORD=

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

RUN apk update
RUN apk add build-base python3 python3-dev py3-pip bash py3-mysqlclient
RUN pip3 install -q --no-cache-dir    \
    Pillow                            \
    channels                          \
    channels_redis                    \
    django                            \
    django-bootstrap-form             \
    ipython                           \
    mysqlclient                       \
    tzdata

#RUN python3 manage.py collectstatic
#VOLUME ["stregsystem"]


EXPOSE 8000:8000
