from logging import getLogger
import re


class Options(object):
    def __init__(self, options=None):
        self.opts = options or {}


class Variables(object):
    """Container substitution variables"""
    logger = getLogger(__name__)
    _pattern = re.compile(r'\{(\w+)\}')

    def __init__(self, variables=None):
        self._variables = variables or {}

    def __iter__(self):
        for k, v in self._variables.iteritems():
            yield k, v

    def get(self, k, default):
        return self._variables.get(k, default)

    def update(self, values):
        for k, v in values:
            self.add_variable(k, v)

    def add_variable(self, key, value):
        if self._variables.get(key, ''):
            self.logger.warn('WARN!!! Variable : %s Already defined!!!', key)
        self._variables[key] = self.expand(value)

    def expand(self, expression):
        """Expands logical constructions."""
        self.logger.debug("expand : expression %s", str(expression))
        if not is_string(expression):
            return expression

        result = self._pattern.sub(lambda var: str(self._variables[var.group(1)]), expression)

        result = result.strip()
        self.logger.debug('expand : %s - result : %s', expression, result)

        if is_number(result):
            if result.isdigit():
                self.logger.debug('     expand is integer !!!')
                return int(result)
            else:
                self.logger.debug('     expand is float !!!')
                return float(result)
        return result


# Module level functions
def is_string(expression):
    #self.logger.debug(" _is_string : %s ", type(expression))
    return expression and (isinstance(expression, unicode) or isinstance(expression, str))


def is_number(expression):
    if is_string(expression):
        expression = expression.strip()
        num_format = re.compile("^[-+]?[0-9]*\.?[0-9]*$")
        return re.match(num_format, expression)
