FROM python:3.10-slim
USER root

#ベースコンテナのセットアップ
RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get -y install gcc g++ libc-dev python3-dev
RUN apt-get -y install vim less mariadb-client
ENV TERM xterm
ENV SHELL /bin/bash
COPY ./container/python/bashrc /root/.bashrc

#R関連のセットアップ
RUN apt-get -y install r-base r-base-dev r-cran-hmisc
ENV R_HOME /usr/lib/R

#python関連のセットアップ
COPY ./requirements.txt /tmp
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r /tmp/requirements.txt

