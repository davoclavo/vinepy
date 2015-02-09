# add check if requests is installed
import requests

from .models import *
from .endpoints import *
from .errors import *

from functools import partial
from json import dumps
import os
import binascii


class API(object):

    def __init__(self, username=None, password=None, device_token=None, DEBUG=False):
        self.username = username
        self.password = password
        self._session_id = None
        self.DEBUG = DEBUG
        self.device_token = device_token or binascii.b2a_hex(os.urandom(32))

        self._make_dynamic_methods()

        if self.username and self.password:
            self.user = self.login(
                username=username, password=password, device_token=self.device_token)

    def _make_dynamic_methods(self):
        for endpoint in list(ENDPOINTS.keys()):
            def _inner(endpoint, *args, **kwargs):
                return self.api_call(endpoint, *args, **kwargs)
            _inner.__name__ = endpoint
            setattr(self, _inner.__name__, partial(_inner, endpoint))

    def build_request_url(self, protocol, host, endpoint):
        url = '%s://%s/%s' % (protocol, host, endpoint)
        # encode url params
        return url

    def api_call(self, endpoint, *args, **kwargs):
        # raise NotImplementedError('API endpoint for method "%s" is not found.' % endpoint)
        meta = ENDPOINTS[endpoint]

        params = self.check_params(meta, kwargs)

        response = self.do_request(meta, params)

        if meta['model'] is None:
            return response
        else:
            model = meta['model'].from_json(response)
            model.connect_api(self)
            return model

    def check_params(self, meta, kwargs):
        missing_params = []
        url_params = []

        # page, size and anchor are data_params for get requests

        for param in meta['url_params']:
            p = kwargs.get(param)
            if p is None:
                missing_params.append(param)
            else:
                url_params.append(p)
                del kwargs[param]
        if missing_params:
            raise ParameterError(
                'Missing URL parameters: [%s]' % ', '.join(missing_params))

        # url_params shouldnt have default params, I guess
        data_params = kwargs
        if meta.get('default_params', []) != []:
            default_params = dict(meta['default_params'])
            data_params = dict(list(default_params.items()) + list(kwargs.items()))

        missing_params = []
        for param in meta['required_params']:
            p = data_params.get(param)
            if p is None:
                missing_params.append(param)
        if missing_params:
            raise ParameterError(
                'Missing required parameters: [%s]' % ', '.join(missing_params))

        # Check for unsupported params?

        return {'url': url_params, 'data': data_params}

    def do_request(self, meta, params):
        headers = HEADERS.copy()
        if params['url'] != []:
            endpoint = meta['endpoint'] % tuple(params['url'])
        else:
            endpoint = meta['endpoint']

        host = API_HOST
        # Upload methods, change host to specific host
        if meta.get('host'):
            host = meta['host']

        url = self.build_request_url(PROTOCOL, host, endpoint)

        built_params = built_data = None
        built_data = data = params['data']

        if meta['request_type'] == 'get':
            built_params = data
        elif meta['request_type'] == 'post':
            if meta.get('json'):
                built_data = dumps(data)
                headers['Content-Type'] = 'application/json; charset=utf-8'
        elif data.get('filename'):
            if data['filename'].split('.')[-1] == 'mp4':
                headers['Content-Type'] = 'video/mp4'
            else:
                headers['Content-Type'] = 'image/jpeg'
            built_data = open(data['filename'], 'rb')

        if self._session_id:
            headers['vine-session-id'] = self._session_id

        if(self.DEBUG):
            # pip install mitmproxy
            # mitmproxy
            http_proxy = "http://localhost:8080"
            https_proxy = "http://localhost:8080"

            proxies = {
                "http": http_proxy,
                "https": https_proxy,
            }

            # cafile='~/.mitmproxy/mitmproxy-ca-cert.pem'
            cafile = False
            response = requests.request(
                meta['request_type'], url, params=built_params, data=built_data, headers=headers, verify=cafile, proxies=proxies)
            print('REQUESTED: %s [%s]' % (url, response.status_code))
        else:
            response = requests.request(
                meta['request_type'], url, params=built_params, data=built_data, headers=headers)

        if response.headers.get('X-Upload-Key'):
            return response.headers['X-Upload-Key']

        if response.status_code in [200, 400, 420]:
            try:
                json = response.json()
            except:
                raise VineError(
                    1000, 'Vine replied with non-json content:\n' + response.text)

            if json['success'] is not True:
                raise VineError(json['code'], json['error'])
            return json['data']
        else:
            raise VineError(response.status_code, response.text)

    def authenticate(self, user):
        self.user = user
        self._session_id = user.key
        self._user_id = user.id
