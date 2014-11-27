from logging import getLogger
from rester.struct import ResponseWrapper
import json
import requests


class HttpClient(object):
    logger = getLogger(__name__)
    ALLOWED_METHODS = ["get", "post", "put", "delete", "patch"]

    def __init__(self, **kwargs):
        self.extra_request_opts = kwargs

    def request(self, api_url, method, headers, params, dump_response):
        is_raw = params.pop('__raw__', False)
        self.logger.debug(
            '\n Invoking REST Call... api_url: %s, method: %s : ', api_url, method)

        try:
            func = getattr(requests, method)
        except AttributeError:
            self.logger.error('undefined HTTP method!!! %s', method)
            raise
        response = func(api_url, headers=headers, params=params, **self.extra_request_opts)

        if is_raw:
            payload = {"__raw__": response.text}
        else:
            payload = response.json()

        if dump_response:
            self.logger.info('JSON response Headers -  %s' + str(response.headers))
            self.logger.info('JSON response -  %s' + json.dumps(
                payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, response.headers)
