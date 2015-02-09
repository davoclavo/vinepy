from datetime import datetime
from functools import reduce

VINE_HASHING_KEY = 'BuzaW7ZmKAqbhMOei5J1nvr6gXHwdpDjITtFUPxQ20E9VY3Ll'
index_key_dict = dict([(char, index)
                       for index, char in enumerate(VINE_HASHING_KEY)])


def post_long_id(short_id):
    prepared_hash = enumerate(short_id[::-1])
    long_id = reduce(lambda acc, index_key: acc + index_key_dict[
                     index_key[1]] * len(VINE_HASHING_KEY) ** index_key[0], prepared_hash, 0)
    return long_id


def post_short_id(long_id):
    id_fragments = int2base(long_id, len(VINE_HASHING_KEY))
    short_id_fragments = map(
        lambda fragment: VINE_HASHING_KEY[fragment], id_fragments)
    return ''.join(short_id_fragments)


def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return 0
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(x % base)
        x //= base
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return digits


def strptime(string, fmt='%Y-%m-%dT%H:%M:%S.%f'):
    return datetime.strptime(string, fmt)

# From http://stackoverflow.com/a/14620633
# CAUTION: it causes memory leak in < 2.7.3 and < 3.2.3


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
