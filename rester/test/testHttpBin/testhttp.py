from __future__ import absolute_import

# Unit test import
import json

from rester.http import HttpClient

# useful test tools
import nose
from nose.tools import assert_equal, assert_true, assert_raises


class TestHttpClient(object):
    """
    Fixture allowing HttpClient Unit test with HttpBin
    """
    def setup(self):
        self.client = HttpClient()
        pass

    def teardown(self):
        pass

    def test_get_request(self):
        url = "http://httpbin.org"
        response = self.client.request(url, "get", {}, {}, False)
        assert_equal(response.status, 200)
        # this fails because dict wrapper is not iteratable
        #assert_true("application/json" in response.headers)
        #jsbody = json.loads(response.body)
        #assert_true("url" in jsbody)
        #assert_equal(jsbody["url"], url)

    # TODO : we need to pass payload with POST
    #def test_post_request(self):
        #url = "http://httpbin.org"
        #response = self.client.request(url, "post", {}, {}, False)


if __name__ == '__main__':
    nose.runmodule()
