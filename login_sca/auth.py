from base64 import b64encode
from collections import namedtuple

from requests import session


def login(username: str, password: bytes, auth_url: str, info_url: str = None):
    """Login to SCA auth system given the user's username and password

    Parameters:

    username (str): Username is the SCA system
    password (bytes): User's password as bytes
    auth_url (str): Authentication endpoint
    info_url (str), optional: User's info endpoint

    Returns:

    resp: namedtuple
        The responses from auth and info requests. The info response
        is optional and only will be executed when the parameters info_url
        if provided.

    """
    s = session()
    resp = s.post(
        auth_url,
        data={
            'username': username,
            'password': b64encode(password).decode('utf-8')
        }
    )

    resp_wrapper = namedtuple('Response', ['auth', 'info'])
    resp_info = None
    if resp.status_code == 200 and info_url is not None:
        resp_info = s.get(info_url)

    return resp_wrapper(resp, resp_info)
