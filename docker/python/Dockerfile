# alpine->slimに変更した理由：
# alpineはPandasのビルドに時間がかかり(最悪30分)、Distro公式もサポートする計画はないため、
# コンテナのメンテナンス性を優先して再度変更。
FROM python:3.10-slim
USER root
WORKDIR /app


#ベースコンテナのセットアップ
RUN apt update
RUN apt -y install busybox coreutils curl bash procps 
RUN apt -y install vim less mariadb-client libmariadb-dev
ENV TERM xterm
ENV SHELL /bin/bash
COPY ./docker/python/bashrc /root/.bashrc

#python関連のセットアップpart1
COPY ./requirements.txt /tmp
RUN apt -y install gcc g++ libc-dev python3-dev
##R関連のセットアップ
##Rpy2のインストールがこけるのでここでやってしまう。
RUN apt -y install r-base r-cran-hmisc
ENV R_HOME /usr/lib/R
#python関連のセットアップpart2
RUN pip install -r /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

#.envファイルの準備
COPY ./src/.env.example /app/.env

#Uvicornの起動
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["uvicorn", "--env-file", "uvicorn.ini", "main:app"]