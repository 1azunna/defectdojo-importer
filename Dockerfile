FROM python:3.13-alpine

LABEL owner="Azunna Ikonne <ikonnea@gmail.com>"
LABEL maintainer="Azunna Ikonne <ikonnea@gmail.com>"

ARG APP_DIR=/app
ARG DATA_DIR=/data
ARG USERNAME=defectdojo-importer

ENV VERSION=0.1

# Perform package updates and create user
# hadolint ignore=DL3018,SC2086
RUN adduser -D -h ${DATA_DIR} -u 1000 ${USERNAME} \
    && mkdir ${APP_DIR} \
    && chown -R ${USERNAME}:${USERNAME} ${DATA_DIR} ${APP_DIR} ;\
    apk update && apk add --no-cache git

WORKDIR ${APP_DIR}
COPY . .
RUN pip install --no-cache-dir wheel poetry ;\
    poetry build ;\
    pip install dist/*.whl

WORKDIR ${DATA_DIR}

USER ${USERNAME}
ENTRYPOINT [ "defectdojo-importer" ]
