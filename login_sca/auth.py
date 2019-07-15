from base64 import b64encode

from requests import session


def login(username, password, auth_url):
    s = session()
    resp = s.post(
        auth_url,
        data={
            'username': username,
            'password': b64encode(password).decode('utf-8')
        }
    )
    return resp
