vinepy
======

*Python wrapper for the [Vine](https://vine.co)  Private API*

## Requirements

* [requests](http://docs.python-requests.org/en/latest/)

## Installation

*I will register this package in the Python Package Index soon*

## Usage

```python
import vinepy

vine = vinepy.API()
user = vine.login(username='email@host.com', password='leinternetz')
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
