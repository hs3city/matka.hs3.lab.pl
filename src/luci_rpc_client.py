from collections import namedtuple
import requests
import random

ApiConnection = namedtuple("ApiConnection", ["url", "cookies"])


def connect(device_url, username, password):
    _id = int(random.random() * 10**9)
    request = {
        "id": _id,
        "method": "login",
        "params": [username, password]
    }
    url = '/'.join([device_url, 'cgi-bin/luci/rpc/auth'])
    response = requests.post(url, json=request)
    assert response.status_code == 200
    return ApiConnection(device_url, response.cookies)


def request(connection, endpoint, method, *params):
    _id = int(random.random() * 10**9)
    request = {
        "id": _id,
        "method": method,
        "params": list(params)
    }
    url = '/'.join([connection.url, 'cgi-bin/luci/rpc', endpoint])
    response = requests.post(url, json=request, cookies=connection.cookies)
    assert response.status_code == 200
    message = response.json()
    assert message['error'] is None, message['error']
    return message['result']


def apply(connection):
    return request(connection, 'uci', 'apply')


def get_changes(connection):
    return request(connection, 'uci', 'changes')


def disconnect(connection):
    url = '/'.join([connection.url, 'cgi-bin/luci/admin/logout'])
    response = requests.get(url, cookies=connection.cookies,  allow_redirects=False)
    assert response.status_code in (200, 302), "problem while closing the " \
                                               "session, http status code: {}".\
                                                format(response.status_code)
