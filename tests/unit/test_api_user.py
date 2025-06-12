from tests.conftest import client


def test_user_login(client):
    rsp = client.post('/api/user/login/')
    assert rsp.status_code == 200

def test_get_users(client):
    pass
