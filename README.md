# MQTTアクセス用テンプレート / MQTT Usage Templae

## 概要 / Overview
このアーカイブに格納されているファイル群はPythonを使って[Beebotte](http://beebotte.com)にMQTTでアクセスするサンプルを提供するものである。
環境を統一するため、Dockerコンテナとして提供する。

Files in this archive show a simple example accessing [Beebotte](http://beebotte.com) using MQTT protocol.
To avoid problems caused by different operating systems, the example is embedded on a docker container.

## ファイル構成 / Files and Directories

ファイル/ディレクトリ | 説明
----- | -----
``src/`` | pythonソースが格納されているディレクトリ。Dockerコンテナ上ではvolumeとしてマウントされる。
``src/client_advanced.py`` | [mqbeebotte](https://github.com/pman0214/mqbeebotte/) を使ったBeebotteアクセスのサンプル。
``src/config.py`` | ``client_advanced.py``用の設定ファイル。**このファイルは絶対にcommitしないこと。**
``docker-compose.yml`` | ``docker-compose``コマンド用の設定YAMLファイル。
``Dockerfile`` | docker環境構築用のDockerfile。
``requirements.txt`` | python環境構築用のライブラリリスト。
``README.md`` | このファイル。

File/Directory | Details
----- | -----
 ``src/`` | is a directory containing python source files.  The docker container mounts the ``src/`` directory as a volume.
``src/client_advanced.py`` | Beebotte access sample using [mqbeebotte](https://github.com/pman0214/mqbeebotte/).
``src/config.py`` | is a config file for ``client_advanced.py``.  **DO NOT COMMIT THIS FILE**.
``docker-compose.yml`` | is a config file for ``docker-compose`` command.
``Dockerfile`` | creates the docker contianer.
``requirements.txt`` | is a list of python libraries.
``README.md`` | is this file.

## 使い方 / Usage

1. docker、docker-composeはあらかじめインストールしておく。
2. 必要であれば``docker-compose.yml``を修正し、初期起動するpythonコードを書いておく。初期状態では何も起動しない。特定のスクリプトを実行する場合はコメントアウトされている``command``行のように記述する。
3. ``docker-compose up -d``する。
4. ちょっと試しに実行したいのであれば``docker-compose exec beebotte /bin/bash``してシェルを起動し、その上でpythonを実行する。なお、``src/``は``/app/src``にマウントされている。
5. 終了したいときは``docker-compose stop``（停止するとき）または``docker-compose down``（停止してdockerコンテナも削除するとき）する。

--

1. Install docker and docker-compose on your machine (or on a target machine).
2. If you want to kick any python script, modify ``docker-compose.yml``.  ``docker-compose.yml`` in this archive does not start any script.  If you want to start a specific script when the container starts, write a start up command on a ``command`` line.
3. Execute ``docker-compose up -d``.
4. If you want to try any python script, execute ``docker-compose exec beebotte /bin/bash`` to start shell on the docker container and then execute any command including python.  Note that ``src/`` directory is mounted on ``/app/src`` as a volume.
5. When you want to stop docker, execute ``docker-compose stop`` (just stopping) or ``docker-compose down`` (stop and remove the container).
