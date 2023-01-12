import json


def test_index(app, client):
    
    response = client.get('/')

    assert response.status_code == 200


def test_userinfo(app, client, username):
    """
    Dado que temos a aplicação configurada para testes
    Quando o endpoint "/user/<username>/info é chamado
    Então deve ser retornado uma resposta válida
    """
    response = client.get(f'/user/{username}/info')

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['account_creation_date'] == '2017-10-26T16:42:29Z'
    assert data['login'] == 'guilhermemaas'
    assert data['username'] == 'Guilherme Augusto Maas'
    
    
def test_userrepos(app, client, username):
    """
    Dado que temos a aplicação configurada para testes
    Quando o endpoint "/user/<username>/repos é chamado
    Então deve ser retornado uma resposta válida
    """
    response = client.get(f'/user/{username}/repos')

    data = json.loads(response.data)

    for repo in data:
       if repo['full_name'] == 'guilhermemaas/cheat-boxes':
           test_repo = repo
       else:
         pass 

    assert response.status_code == 200
    assert test_repo['creation_date'] == '2020-05-19T19:27:57Z'


def test_usergists(app, client, username):
    """
    Dado que temos a aplicação configurada para testes
    Quando o endpoint "/user/<username>/gists é chamado
    Então deve ser retornado uma resposta válida
    """
    response = client.get(f'/user/{username}/gists')

    data = json.loads(response.data)

    for gist in data:
       if gist['id'] == '806e5ac621160cd946861d30b4152d79':
           test_gist = gist
       else:
         pass 

    assert response.status_code == 200
    assert test_gist['creation_date'] == '2021-01-01T10:49:53Z'


def test_usercommits(app, client, username):
    """
    Dado que temos a aplicação configurada para testes
    Quando o endpoint "/user/<username>/commits é chamado
    Então deve ser retornado uma resposta válida
    """

    response = client.get(f'/user/{username}/commits')
    
    assert response.status_code == 200