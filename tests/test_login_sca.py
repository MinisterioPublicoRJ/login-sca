from unittest import mock

from login_sca.auth import login


@mock.patch('login_sca.auth.session')
def test_successful_login(_session):
    """Should create a session with requests and make a post to auth_url
    with user credentials"""

    resp_mock = mock.MagicMock(status_code=200, content=b'')
    session_mock = mock.MagicMock()
    session_mock.post.return_value = resp_mock
    _session.return_value = session_mock

    username = 'username'
    password = b'password'
    auth_url = 'http://auth.com'

    resp = login(username=username, password=password, auth_url=auth_url)
    expected_data = {'username': username, 'password': 'cGFzc3dvcmQ='}

    assert resp.status_code == 200
    session_mock.post.assert_called_once_with(
        auth_url,
        data=expected_data
    )
