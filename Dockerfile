# Build stage
FROM python:3.13-alpine AS builder

ARG APP_DIR=/app

WORKDIR ${APP_DIR}

# Install build dependencies
RUN apk update && apk add --no-cache git build-base

# Copy source and build configuration
COPY . .

# Build the wheel
RUN pip install --no-cache-dir wheel poetry && \
    poetry build -f sdist

# Runtime stage
FROM python:3.13-alpine AS runtime

LABEL owner="Azunna Ikonne <ikonnea@gmail.com>"
LABEL maintainer="Azunna Ikonne <ikonnea@gmail.com>"

ARG DATA_DIR=/data
ARG USERNAME=defectdojo-importer

# Create user and directories
RUN adduser -D -h ${DATA_DIR} -u 1000 ${USERNAME} && \
    chown -R ${USERNAME}:${USERNAME} ${DATA_DIR}

# Copy built wheel from builder stage
COPY --from=builder /app/dist/*.whl /tmp/

# Install the application
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*.whl

WORKDIR ${DATA_DIR}
USER ${USERNAME}

ENTRYPOINT ["defectdojo-importer"]
