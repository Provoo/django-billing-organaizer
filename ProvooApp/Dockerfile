FROM python:2.7

ARG DJANGO_ENV

USER root

ENV PYTHONUNBUFFERED=1
ENV WEBAPP_DIR=/ProvooApp

RUN mkdir $WEBAPP_DIR
RUN chmod 755 -R $WEBAPP_DIR

WORKDIR $WEBAPP_DIR

ADD requirements/base.txt $WEBAPP_DIR/
ADD requirements/$DJANGO_ENV.txt $WEBAPP_DIR/
COPY start.sh $WEBAPP_DIR/

RUN pip install -r $DJANGO_ENV.txt

#Mapeo del proyecto
ADD . $WEBAPP_DIR/
