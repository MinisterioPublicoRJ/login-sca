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

    resp, info = login(username=username, password=password, auth_url=auth_url)
    expected_data = {'username': username, 'password': 'cGFzc3dvcmQ='}

    assert resp.status_code == 200
    assert resp.content == b''
    session_mock.post.assert_called_once_with(
        auth_url,
        data=expected_data
    )


@mock.patch('login_sca.auth.session')
def test_return_users_info(_session):
    "Should return a 200 status code and user's info"

    expected_body = '{"username":"anyusername.auth","permissions":{"role_1":'\
                    'true,"role_2":true,"role_3":true},'\
                    '"userDetails":{"detail_key_1": "detail_value_1",'\
                    '"detailt_key_2": "detail_value_2"}'
    expected_info = {
        'username': 'anyusername',
        'permissions': {'role_1': True, 'role_2': True, 'role_3': True},
        'userDetails': {'detail_key_1': 'detail_value_1',
                        'detail_key_2': 'detail_value_2'}
    }

    resp_post_mock = mock.MagicMock(
        status_code=200,
        content=b''
    )
    resp_get_mock = mock.MagicMock(
        status_code=200,
        content=expected_body
    )
    resp_get_mock.json.return_value = expected_info

    username = 'username'
    password = b'password'
    auth_url = 'http://auth.com'
    info_url = 'http://info.com'

    session_mock = mock.MagicMock()
    session_mock.post.return_value = resp_post_mock
    session_mock.get.return_value = resp_get_mock
    _session.return_value = session_mock

    resp, info = login(
        username=username,
        password=password,
        auth_url=auth_url,
        info_url=info_url
    )

    assert resp.status_code == 200
    assert info == expected_info


@mock.patch('login_sca.auth.session')
def test_login_failure(_session):
    resp_mock = mock.MagicMock(
        status_code=401,
        content=b'<html>auth failed</html>'
    )
    session_mock = mock.MagicMock()
    session_mock.post.return_value = resp_mock
    _session.return_value = session_mock

    username = 'wrong_username'
    password = b'wrong_password'
    auth_url = 'http://auth.com'
    info_url = 'http://info.com'

    resp, info = login(
        username=username,
        password=password,
        auth_url=auth_url,
        info_url=info_url
    )

    assert resp.status_code == 401
    assert resp.content == b'<html>auth failed</html>'
    session_mock.get.assert_not_called()
