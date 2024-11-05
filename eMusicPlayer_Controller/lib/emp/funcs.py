
from requests import get


def get_public_ip():
    return get('https://api.ipify.org').content.decode('utf8')