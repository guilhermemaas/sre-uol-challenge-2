import json 


def test_index(app, client):
    
    response = client.get('/')

    assert response.status_code == 200


def test_userinfo(app, client):
    
    response = client.get('/userinfo/guilhermemaas')

    assert response.status_code == 200


def test_userrepos(app, client):
    
    response = client.get('/userrepos/guilhermemaas')
    
    assert response.status_code == 200


def test_usergists(app, client):
    
    response = client.get('/usergists/guilhermemaas')
    
    assert response.status_code == 200


def test_usercommits(app, client):
    
    response = client.get('/usercommits/guilhermemaas')
    
    assert response.status_code == 200