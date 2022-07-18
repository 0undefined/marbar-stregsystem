FROM alpine:3.16.0

WORKDIR /usr/share/www

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add build-base python3 python3-dev py3-pip bash
RUN pip3 install -q --no-cache-dir    \
    Pillow                            \
    channels                          \
    channels_redis                    \
    django                            \
    django-bootstrap-form             \
    ipython                           \
    tzdata

#RUN python3 manage.py collectstatic
#VOLUME ["stregsystem"]


EXPOSE 8000:8000
