
from requests import get

import typing
if typing.TYPE_CHECKING:
    pass


# DEPRECATED
"""
def get_key_from_value(dict_: dict, value):
    return tuple(dict_.keys())[tuple(dict_.values()).index(value)]
"""


def get_public_ip():
    return get('https://api.ipify.org').content.decode('utf8')


def get_file_name(string: str):
    """Return file name w/ extension from a file path"""
    return string[-string[::-1].find('\\'):-string[::-1].find('.')-1]


def filter_1(function: typing.Callable, iterable: typing.Iterable):
    """Return the first item of iterable which function(item) returns True, else None"""

    t = tuple(filter(function, iterable))

    try:
        return t[0]

    except IndexError:
        return None


def hyperlist(value=None, *args: int):

    return [(hyperlist(value, *args[1:]) if len(args) > 1 else value)
            for i in range(args[0])
            ]


def group(iterable: typing.Iterable, n: int):
    """s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."""
    return zip(*[iter(iterable)] * n)
