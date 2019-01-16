<a href="http://cpchain.io"><img src="https://cpchain.io/static/img/logo_new.svg" title="cpchain.io" alt="cpchain.io"></a>



# CpchainWebsite

> Including CPCHAIN.IO and EXPLORER of CPCHAIN.

![](https://img.shields.io/badge/language-python3-orange.svg)![](https://img.shields.io/codeclimate/coverage/jekyll/jekyll.svg)[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)[![Pull Requests](https://img.shields.io/bitbucket/pr-raw/cpchain/chain.svg)](https://bitbucket.org/cpchain/chain/pull-requests/)[![Follow Twitter](https://img.shields.io/twitter/follow/cpchain_io.svg?label=Follow&style=social)](https://twitter.com/intent/follow?screen_name=cpchain_io)


## What is Cpchain?
CPChain is a new distributed infrastructure for next generation IoT. CPChain intends to build a fundamental data platform for IoT systems in combination with distributed storage, encryption computation and blockchain technologies, providing the whole process solution from data acquisition, storage, sharing to application.

CPChain is a promising solution to a series of challenges of the current "chimney architecture" of IoT systems, reducing connectivity cost of devices, protecting data privacy and maximizing the value of IoT data.




## Installation

### Clone

Clone this repo to your local machine using `git clone https://github.com/CPChain/cpchain-website.git`

### Setup


> update and install the requirements first
```python3
pip3 install -r requirements.txt
```
> change your settings in config.default.ini
```ini
[chain]
ip=127.0.0.1
port=8501

[db]
ip=127.0.0.1 #mongodb
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
Now You can access http://127.0.0.1:8000/
```


### Note:

For testing Cpchain API functions, it would be best to setup a private network on your local machine using the <a href="http://docs.cpchain.io/deployment/deployment.html#download-docker" target="_blank">CPCHAIN Docker Guide</a>. The Docker guide sets up a Full Node and Event Server on your machine. 
You can then deploy smart contracts on your network and interact with them via CPChainWeb. 





## Documentation 

The website uses a third-party package cpc-fusion. For more detailed information, please see here:
<a href='http://docs.cpchain.io/api/cpc_fusion.cpc.html'>cpc-fusion</a>

---




## License

- Copyright 2018 © <a href="https://cpchain.io" target="_blank">cpchain.io</a>.

