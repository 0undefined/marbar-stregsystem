FROM alpine:3.21.3
#FROM alpine:3.16.0


ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

RUN apk update
RUN apk add build-base sqlite python3 python3-dev py3-pip bash py3-mysqlclient
RUN pip3 install --break-system-packages -q --no-cache-dir    \
    Pillow                            \
    channels-redis==4.2.1             \
    channels["daphne"]                \
    django==4.2                            \
    django-csp                        \
    gunicorn                          \
    ipython                           \
    tzdata


COPY ./gunicon.py /usr/share/gunicorn-conf.py
ADD ./stregsystem/ /usr/share/www/
WORKDIR /usr/share/www

RUN mkdir -p /usr/share/www/static


COPY ./runserver.sh /usr/bin
RUN [ "chmod", "+x", "/usr/bin/runserver.sh" ]

EXPOSE 8000:8000

CMD [ "/usr/bin/env", "sh", "./runserver.sh" ]
#ENTRYPOINT [ "runserver.sh" ]
