FROM python:3.10

ADD . /app
WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install --with dev

ENV DOCKERIZE_VERSION v0.6.1
RUN curl -qsL https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar -C /usr/local/bin -xzvvf -

