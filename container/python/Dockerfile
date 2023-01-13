FROM python:3.10-alpine
USER root
WORKDIR /app

#ベースコンテナのセットアップ
RUN apk update
RUN apk add bash busybox coreutils curl
RUN apk add bash 
RUN apk add gcc g++ libc-dev python3-dev
RUN apk add vim less mariadb-client
ENV TERM xterm
ENV SHELL /bin/bash
COPY ./container/python/bashrc /root/.bashrc

#R関連のセットアップ
RUN apk add R R-dev
ENV R_HOME /usr/lib/R

#python関連のセットアップ
COPY ./requirements.txt /tmp
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r /tmp/requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]