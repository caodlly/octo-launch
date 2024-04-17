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

# ==Build Stage 2=====================================================
FROM docker.io/python:3.11.7-slim-bookworm as python-run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENVIRONMENT ${BUILD_ENVIRONMENT}

ARG APPHOME=/app

WORKDIR ${APPHOME}
# Install wget, gnupg, and software-properties-common
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Download the GPG key and add it to the keyring
RUN wget -qO - 'https://proget.makedeb.org/debian-feeds/prebuilt-mpr.pub' \
    | gpg --dearmor \
    | tee /usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg 1> /dev/null

# Add the repository to the APT sources list
RUN echo "deb [arch=all,$(dpkg --print-architecture) signed-by=/usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg] https://proget.makedeb.org prebuilt-mpr $(lsb_release -cs)" \
    | tee /etc/apt/sources.list.d/prebuilt-mpr.list

# Update APT package lists and install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    just \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Clean up unused files
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false


COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

EXPOSE 8080


COPY ./shell/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY . ${APPHOME}
