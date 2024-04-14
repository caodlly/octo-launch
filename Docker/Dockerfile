# Build Stage 1
FROM docker.io/python:3.11.7-slim-bookworm as python-build-stage


# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev
ARG BUILD_ENVIRONMENT
COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt

# Build Stage 2
FROM docker.io/python:3.11.7-slim-bookworm as python-run-stage


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENVIRONMENT ${BUILD_ENVIRONMENT}

ARG APPHOME=/app

WORKDIR ${APPHOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

EXPOSE 8080


COPY ./shell/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY . ${APPHOME}
