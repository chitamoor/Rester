

class DictWrapper(object):
    def __init__(self, d):
        for key, value in d.items():
            if isinstance(value, (list, tuple)):
                setattr(
                    self, key, [DictWrapper(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, DictWrapper(value)
                        if isinstance(value, dict) else value)

    def get(self, name, default):
        return self.__dict__.get(name, default)

    def __getattr__(self, name):
        levels = name.split(".")
        if len(levels) > 1:
            curr_level = levels.pop(0)
            return getattr(self.__dict__[curr_level], '.'.join(levels))
        else:
            #print "name : " + name
            return self.__dict__[name] # if name in self.__dict__ else None

    def __setattr__(self, key, value):
        self.__dict__[key] = DictWrapper(value) if isinstance(value, dict) else value

    def items(self):
        return self.__dict__


class ResponseWrapper(object):
    def __init__(self, status, data, headers):
        self.status = status
        self.body = DictWrapper(data)
        self.headers = DictWrapper(headers)
