# CPChain Website

![logo](https://github.com/CPChain/cpchain-website/blob/master/static/img/logo_new.svg)

> Including CPCHAIN.IO and EXPLORER of CPCHAIN.

![lang](https://img.shields.io/badge/language-python3-orange.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Pull Requests](https://img.shields.io/bitbucket/pr-raw/cpchain/chain.svg)](https://github.com/CPChain/cpchain-website/pulls)
[![Follow Twitter](https://img.shields.io/twitter/follow/cpchain_io.svg?label=Follow&style=social)](https://twitter.com/intent/follow?screen_name=cpchain_io)

## What is CPChain

CPChain is a new distributed infrastructure for next generation IoT. CPChain intends to build a fundamental data platform for IoT systems in combination with distributed storage, encryption computation and blockchain technologies, providing the whole process solution from data acquisition, storage, sharing to application.

CPChain is a promising solution to a series of challenges of the current "chimney architecture" of IoT systems, reducing connectivity cost of devices, protecting data privacy and maximizing the value of IoT data.

## Installation

### Clone

Clone this repo to your local machine using `git clone https://github.com/CPChain/cpchain-website.git`

### Setup

Update and install the requirements first

```python3

pip3 install -r requirements.txt

```

Change your settings in config.default.ini

```ini

[chain]
ip=127.0.0.1
port=8501

[db]
ip=127.0.0.1 #mongodb

```

```bash

# start database
docker-compose up -d mysql mongo

# start monitor
docker-compose up -d monitor

# collect static
docker-compose run collect-static

# start test-container if you are developing or testing
docker-compose up dev

# create super user in test-env
docker exec -it cpchain-website_test_1 python manage.py createsuperuser

# username: admin
# password: 123456

# start daphne and nginx
docker-compose up -d daphne

# cleanup ip access table
python manage.py cleanup

```

### Start Celery

```bash

# start worker
celery worker -A tasks.app

# beat start
celery beat -A tasks.app

```

---

## Start

> To run this website with explorer of cpchain ,you need to install mongodb to save the data from chain.

run db monitor :

```python
python3 db_monitor.py
```

There are two modes to start this website , through http or socket(default):

```shell

./uwsgi_reload.sh http
[Mode]http
[uWSGI] getting INI configuration from uwsgi.ini
[uwsgi-static] added mapping for /static => ./static

```

Now You can access [localhost](http://127.0.0.1:8000/)

## Documentation

The website uses a third-party package cpc-fusion. For more detailed information, please see here:
[cpc-fusion](https://docs.cpchain.io/api/cpc_fusion.html)

---

## License

- Copyright 2019 © [cpchain.io](https://cpchain.io).
