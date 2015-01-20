vinepy
======

*Python wrapper for [Vine](https://vine.co) API*

## Requirements

* [requests](http://docs.python-requests.org/en/latest/)

## Installation

`pip install vinepy`

## Usage

```python
import vinepy

vine = vinepy.API(username='email@host.com', password='leinternetz')
user = vine.user
followers = user.followers()
timeline = user.timeline()
```

## Documentation

*Work in progress*

## Acknowledgements

* Inspired on [TweetPony](https://github.com/Mezgrman/TweetPony)
* Based on the Vine API documentation by [neuegram](https://github.com/neuegram/vineapi) and [starlock](https://github.com/starlock/vino/wiki/API-Reference)
* Used [mitmproxy](http://mitmproxy.org/) to get the missing API endpoints
* Thanks to [Vine](https://vine.co) for making such an amazing app.
