# base image
FROM python:3.11.6-slim-bullseye

# setting ENV
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# work dir
WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN pip install pipenv && pipenv install --system

COPY . /code/
