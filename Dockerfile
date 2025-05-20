FROM python:3.11.7-slim-bullseye

ENV PYTHONPATH "${PYTHONPATH}:/opt"

COPY ./src /opt/
WORKDIR /opt

# Install requirements
RUN set -x \
    && pip install --upgrade setuptools==69.0.2 \
    && pip install --upgrade pip \
    && pip install --upgrade pip-tools \
    && pip-sync requirements.txt

