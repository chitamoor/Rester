from __future__ import absolute_import

# Unit test import
from rester.struct import DictWrapper

# useful test tools
import nose
from nose.tools import assert_equal, assert_true, assert_raises


# testing multiple ways to initialize dict wrapper
def testdictwrapper_init():
    dw = DictWrapper({"testkey": "testvalue"})
    # breaking : dictwrapper not iteratable
    #assert_true("testkey" in dw)
    # no attribute __getitem__
    #assert_equal(dw["testkey"], "testvalue")
    assert_equal(dw.get("testkey", "notthere"), "testvalue")


class TestDictWrapper(object):
    """
    Fixture allowing DictWrapper manipulations unit testing
    """
    def setup(self):
        self.dictwrapper = DictWrapper({"testkey": "testvalue"})
        pass

    def teardown(self):
        pass

    def test_get_testkey(self):
        assert_equal(self.dictwrapper.get("testkey", "notthere"), "testvalue")


if __name__ == '__main__':
    nose.runmodule()
