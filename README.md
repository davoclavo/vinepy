[![](https://travis-ci.org/davoclavo/vinepy.svg?branch=master)](https://travis-ci.org/davoclavo/vinepy)


vinepy
======

*Python wrapper for the [Vine](https://vine.co) API*


## Installation

From Github

```sh
git clone https://github.com/davoclavo/vinepy.git
cd vinepy
python setup.py install
```

From PyPi

```sh
pip install vinepy
```

## Requirements

* [requests](http://docs.python-requests.org/en/latest/)
* [nose2](https://github.com/nose-devs/nose2)
* [vcrpy](https://github.com/kevin1024/vcrpy)


## Usage

```python
import vinepy

vine = vinepy.API(username='email@host.com', password='leinternetz')
user = vine.user
followers = user.followers()
timeline = user.timeline()
```

## Run tests

```sh
cd vinepy
nose2
```

## Documentation

*Work in progress*

## Acknowledgements

* Inspired on [TweetPony](https://github.com/Mezgrman/TweetPony)
* Based on the Vine API documentation by [neuegram](https://github.com/neuegram) and [starlock](https://github.com/starlock/vino/wiki/API-Reference)
* Used [mitmproxy](http://mitmproxy.org/) to get the missing API endpoints
* Thanks to [Vine](https://vine.co) for making such an amazing app.
