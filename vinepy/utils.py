from datetime import datetime

def strptime(string, fmt='%Y-%m-%dT%H:%M:%S.%f'):
    return datetime.strptime(string, fmt)

# From http://stackoverflow.com/a/14620633
# CAUTION: it causes memory leak in < 2.7.3 and < 3.2.3
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
