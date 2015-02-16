vinepy
======

*Python wrapper for the [Vine](https://vine.co) API*

[![](https://travis-ci.org/davoclavo/vinepy.svg?branch=master)](https://travis-ci.org/davoclavo/vinepy)
[![](https://img.shields.io/coveralls/davoclavo/vinepy.svg)](https://coveralls.io/r/davoclavo/vinepy)
[![](https://img.shields.io/pypi/v/vinepy.svg)](https://pypi.python.org/pypi/vinepy)
[![](https://img.shields.io/badge/coolness-ultrasupercool-blue.svg)](http://i.imgur.com/oJ6ZZf8.gif)

## Installation

From pip

```
pip install vinepy
```

From source

```
git clone https://github.com/davoclavo/vinepy.git
cd vinepy
pip install -r dev-requirements.txt
python setup.py install
```

## Requirements

#### Usage

* [requests](http://docs.python-requests.org/en/latest/)

#### Development

* [nose2 + coverage-plugin](https://github.com/nose-devs/nose2)
* [vcrpy](https://github.com/kevin1024/vcrpy)


## Examples

```python
import vinepy

vine = vinepy.API(username='email@host.com', password='leinternetz')
user = vine.user
followers = user.followers()
timeline = user.timeline()
```

## Tests

#### Quick run tests
```sh
cd vinepy
nose2
```

#### Coverage
```sh
cd vinepy
nose2 --with-coverage --coverage-report html
open htmlcov/index.html
```


## Acknowledgements

* Inspired on [TweetPony](https://github.com/Mezgrman/TweetPony)
* Based on the Vine API documentation by [neuegram](https://github.com/neuegram) and [starlock](https://github.com/starlock/vino/wiki/API-Reference)
* Used [mitmproxy](http://mitmproxy.org/) to get the missing API endpoints
* Thanks to [Vine](https://vine.co) for making such an amazing app.
