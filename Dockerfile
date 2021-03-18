########
# This image compile the dependencies
########
FROM python:3.8-slim as compile-image


ENV VIRTUAL_ENV /srv/venv
ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /srv

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    binutils \
    build-essential \
    libpq-dev \
    && apt-get autoremove --purge -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv ${VIRTUAL_ENV}

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

########
# This image is the runtime
########
FROM python:3.8-slim as runtime-image

ARG VERSION_SHA
ARG VERSION_NAME
ENV VERSION_SHA $VERSION_SHA
ENV VERSION_NAME $VERSION_NAME

ENV VIRTUAL_ENV /srv/venv
ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /srv

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    libpq-dev \
    && apt-get autoremove --purge -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd uwsgi
RUN useradd --no-log-init -g uwsgi uwsgi

# Copy venv with compiled dependencies
COPY --chown=uwsgi:uwsgi --from=compile-image /srv/venv /srv/venv

COPY --chown=uwsgi:uwsgi ["docker-entrypoint.sh", "uwsgi.ini", "manage.py", "/srv/"]
COPY --chown=uwsgi:uwsgi . /srv
RUN chmod +x docker-entrypoint.sh

ENV FILES_ROOT /var/www
RUN mkdir -p "${FILES_ROOT}"
RUN chown uwsgi:uwsgi "${FILES_ROOT}"

USER uwsgi
EXPOSE 8000

ENTRYPOINT ["/srv/docker-entrypoint.sh"]