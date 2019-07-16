# Simple module for SCA system login

This is a Python module which wraps the necessary resquests
to the SCA system.

If both Authentication and Information are provided the function
will login and then retrieve information about the user in the system.

In case only Authentication URL is given, login is executed but no other
information is returned.

```python
from login_sca import login

auth_url = 'http://auth.com'
info_url = 'http://info.com'

resp = login('username', b'password', auth_url, info_url)
print(resp)
Response(auth=<Response [200]>, info=<Response [200]>)

print(resp.auth.status_code)
200

print(resp.info.json())

{'username': 'Nome do usuário',
 'permissions': {
     'role_1': True,
     'role_2': True

 }
}
```
