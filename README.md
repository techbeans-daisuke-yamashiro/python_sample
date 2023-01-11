### 必要ライブラリのインストール
requirements.txtに記載しているので、pipでインストールする。
```
$ pip install -r requirements.txt 
```


#### 依存パッケージのインストール
利用しているPandas、Num.pyが下記に依存しているのでインストールする必要がある。
- python3-dev
- gcc
- g++
- libc-dev
- linux-headers

##### Alpine Linuxの場合
``` bash
$ sudo apk --update-cache add python3-dev gcc g++ libc-dev linux-headers
```

##### Ubuntu22.04の場合
build-essencialを利用するとよい。
``` bash
$ sudo apt install -y build-essencial python3-dev linux-headers
```