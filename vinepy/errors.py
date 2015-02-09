class VineError(Exception):

    def __init__(self, code, error):
        self.code = code
        self.error = error

    def __str__(self):
        return '#%i: %s' % (self.code, self.error)


class ParameterError(Exception):

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description
