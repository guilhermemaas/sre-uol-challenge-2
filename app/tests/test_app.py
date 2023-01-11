import json 


def test_index(app, client):
    
    response = client.get('/')

    assert response.status_code == 200


def test_userinfo(app, client):
    
    response = client.get('/user/guilhermemaas/info')

    assert response.status_code == 200


def test_userrepos(app, client):
    
    response = client.get('/user/guilhermemaas/repos')
    
    assert response.status_code == 200


def test_usergists(app, client):
    
    response = client.get('/user/guilhermemaas/gists')
    
    assert response.status_code == 200


def test_usercommits(app, client):
    
    response = client.get('/user/guilhermemaas/commits')
    
    assert response.status_code == 200