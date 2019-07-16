from base64 import b64encode

from requests import session


def login(username: str, password: bytes, auth_url: str, info_url: str = None):
    """Login to SCA auth system given the user's username and password

    Parameters:

    username (str): Username is the SCA system
    password (bytes): User's password as bytes
    auth_url (str): Authentication endpoint

    """
    s = session()
    resp = s.post(
        auth_url,
        data={
            'username': username,
            'password': b64encode(password).decode('utf-8')
        }
    )

    resp_info = None
    if resp.status_code == 200 and info_url is not None:
        resp_info = s.get(info_url)

    return resp, resp_info
