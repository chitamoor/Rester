from rester.struct import DictWrapper
import json
import os
import yaml
from rester.manifest import Variables


class TestSuite(object):
    def __init__(self, filename):
        self.filename = filename
        self.test_cases = []
        self.variables = Variables()
        self.load()

    def load(self):
        with open(self.filename) as fh:
            data = load(self.filename, fh)
            self._load(data)

    def _load(self, data):
        self.variables.update(data.get('globals', {}).get('variables', {}).items())
        for case in data['test_cases']:
            filename = os.path.join(os.path.dirname(self.filename), case)
            self.test_cases.append(TestCase(self, filename))


class TestCase(object):
    def __init__(self, suite, filename):
        self.filename = filename
        self.data = None
        self.variables = Variables()
        if suite:
            self.variables.update(suite.variables)
        self.load()

    def __getattr__(self, key):
        return getattr(self.data, key)

    @property
    def steps(self):
        return self.data.testSteps

    @property
    def request_opts(self):
        return self.variables.get('request_opts', {})

    def load(self):
        with open(self.filename) as fh:
            data = load(self.filename, fh)
            self._load(data)

    def _load(self, data):
        self.data = DictWrapper(data)
        self.variables.update(data.get('globals', {}).get('variables', {}).items())


def load(filename, fh):
    if filename.endswith(".yaml"):
        return yaml.load(fh.read())
    return json.load(fh)
