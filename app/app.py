import requests
import pytest 
import json
from flask import Flask, request, jsonify, render_template
from flask.wrappers import Response
from prometheus_flask_exporter import PrometheusMetrics
from operator import itemgetter
import logging 
import os
from datetime import date
from flasgger import Swagger
from flasgger.utils import swag_from

class GitHubApi:
    def __init__(self, github_user: str, github_base_URL: str):
        self.github_user = github_user
        self.github_base_URL = github_base_URL

    def get_github_user_info(self) -> dict:
        """
        Retorna todos os dados de um usuário público do Github através do endpoint /users
        """
        
        URL = f'{self.github_base_URL}/users/{self.github_user}'
        
        response = requests.get(URL)
        
        return response.json()

    def get_github_user_repos(self) -> list:
        """
        Retorna todos os repositórios públicos de um usuário do Github
        """
        
        URL = f'{self.github_base_URL}/users/{self.github_user}/repos'
        
        response = requests.get(URL)
        
        return response.json()

    def get_github_user_gists(self) -> list:
        """
        Retorna todos os gists públicos de um usuário do Github
        """
        
        URL = f'{self.github_base_URL}/users/{self.github_user}/gists'
        
        response = requests.get(URL)
        
        return response.json()

    def get_github_user_commits(self) -> list:
        """
        Retorna todos os commits de um repositório, do mais novo para o mais antigo
        Exemplo:
        https://api.github.com/repos/guilhermemaas/container-expert-linuxtips/commits
        """

        URL = f'{self.github_base_URL}/users/{self.github_user}/repos'

        response = requests.get(URL)

        github_user_repos = response.json()

        github_repos_commits_urls = []

        for repo in github_user_repos:
            if 'sha' in repo['commits_url']:
                repo['commits_url'] = repo['commits_url'].replace('{/sha}','')
                print(f'COMMIT_URL:{repo["commits_url"]}')
                github_repos_commits_urls.append(repo['commits_url'])
            else:
                pass

        github_user_commits_default = []

        for commit_url in github_repos_commits_urls:
            print(f'commit: {commit_url}')
            github_user_commits_default.append(requests.get(commit_url).json())
        
        #print(github_user_commits_default)

        return github_user_commits_default


app = Flask(__name__)

#Gera o endpoint /metrics utilizando o Flask Prometheus Exporter
metrics = PrometheusMetrics(app)

#Gera a documentação com Swagger utilizando o Flasgger
swagger = Swagger(app)

github_BASE_URL = 'https://api.github.com'

@app.route('/')
@app.route('/home')
@app.route('/index')
@app.route('/entry')
def index():
    """
    Página default ao chamar URL's "raíz"
    """

    return render_template('index.html',
        the_tittle=f'SRE UOL - Challenge 2: API Git Hub - Data: {date.isoformat(date.today())}')


@app.route('/userinfo/<username>', methods=['GET'])
@swag_from("swagger/userinfo.yml")
def userinfo(username):
    """
    Esse endpoint retorna os seguintes dados de um usuário do Git Hub, em formato JSON:
    - Login do usuário
    - Nome do usuário
    - E-mail do usuário
    - Bio (Se esta informação estiver preenchida pelo usuário)
    - URL para o avatar do usuário
    - Quantidade de repositórios públicos
    - Quantidade de gists públicos
    - Quantidade de usuários seguidores
    - Quantidade de usuários que está seguindo
    - Data de criação da conta
    """
    
    #Recebe a informação vinda da chamada em formato .json
    #content = request.json
    
    #github_username = content['github_username']
    #github_username = github_username

    github_username = username

    #Instância um objeto para chamada na api do Git Hub contendo as informações de usuário URL base do Git Hub
    github_request = GitHubApi(github_username, github_BASE_URL)
    
    #Recebe um dicionário de dados com as informações padrão da API do Git Hub (/users)
    github_user_info_default = github_request.get_github_user_info()

    #Ajusta um dicionário temporário somente os campos que queremos retornar na API
    github_user_info = {
        'login':  github_user_info_default['login'],
        'username': github_user_info_default['name'],
        'email': github_user_info_default['email'],
        'bio': github_user_info_default['bio'],
        'avatar_url': github_user_info_default['avatar_url'],
        'qt_public_repos': github_user_info_default['public_repos'],
        'qt_public_gists': github_user_info_default['public_gists'],
        'qt_followers': github_user_info_default['followers'],
        'qt_following': github_user_info_default['following'],
        'account_creation_date': github_user_info_default['created_at']
    }

    #Retorna as informações dos campos citados acima
    return jsonify(github_user_info)


@app.route('/userrepos/<username>', methods=['GET'])
@swag_from("swagger/userrepos.yml")
def userrepos(username):
    """
    Esse endpoint retorna os seguintes dados referentes aos repositórios de um
    usuário do Git Hub, em formato JSON:
    - Nome do repositório
    - ID do repositório
    - Nome completo do repositório
    - Descrição do repositório
    - Login do owner/dono do repositório
    - URL git do repositório
    - URL ssh do repositório
    - URL com listagem de commits no repositório
    - Data de criação
    - Último push/alteração
    - Branch default/padrão
    - Número de Issues em aberto
    """
    
    #Recebe a informação vinda da chamada em formato .json
    #content = request.json
    
    #github_username = content['github_username']
    github_username = username

    #Instância um objeto para chamada na api do Git Hub contendo as informações de usuário URL base do Git Hub
    github_request = GitHubApi(github_username, github_BASE_URL)
    
    #Recebe um dicionário de dados com as informações padrão da API do Git Hub (/users)
    github_user_repos_default = github_request.get_github_user_repos()

    github_user_repos = []
    github_temp_repo = {}

    #Percore a lista de repositórios retornado pela API do Git Hub adicionando a um dicionário temporário os 
    #campos desejados
    for repo in github_user_repos_default:
        github_temp_repo = {
            'name': repo['name'],
            'id': repo['id'],
            'full_name': repo['full_name'],
            'description': repo['description'],
            'owner': repo['owner']['login'],
            'git_url': repo['git_url'],
            'ssh_url': repo['ssh_url'],
            'commits_url': repo['commits_url'],
            'creation_date': repo['created_at'],
            'latest_push': repo['pushed_at'],
            'default_branch': repo['default_branch'],
            'qt_open_issues': repo['open_issues']
        }

        #Adiciona o repositório em questão à lista que será retornanda no endpoint
        github_user_repos.append(github_temp_repo.copy())

        #Limpa o dicionário temporário utilizado para percorrer a lista retornada pela API do Git Hub
        github_temp_repo.clear()

    #Ordena a lista em ordem alfabética para apresentação
    github_user_repos = sorted(github_user_repos, key=itemgetter('name'), reverse=False)

    #Retorna as informações dos campos citados acima
    return jsonify(github_user_repos)


@app.route('/usergists/<username>', methods=['GET'])
@swag_from("swagger/usergists.yml")
def usergists(username):
    """
    Esse endpoint retorna os seguintes dados referentes aos gists de um
    usuário do Git Hub, em formato JSON:
    - ID do gist
    - URL do gist
    - Arquivo(s)
    - Owner/Dono do gist
    - Data/Hora de criação
    - Data/Hora de última atualização
    """
    
    #Recebe a informação vinda da chamada em formato .json
    #content = request.json
    
    #github_username = content['github_username']
    github_username = username

    #Instância um objeto para chamada na api do Git Hub contendo as informações de usuário URL base do Git Hub
    github_request = GitHubApi(github_username, github_BASE_URL)
    
    #Recebe um dicionário de dados com as informações padrão da API do Git Hub (/users)
    github_user_gists_default = github_request.get_github_user_gists()

    #Ajusta um dicionário temporário somente os campos que queremos retornar na API

    github_user_gists = []
    github_temp_gist = {}

    for gist in github_user_gists_default:
        github_temp_gist = {
            'id': gist['id'],
            'url': gist['url'],
            'files': gist['files'],
            'owner': gist['owner']['login'],
            'creation_date': gist['created_at'],
            'latest_update': gist['updated_at'],
        }

        #Adiciona o gist em questão à lista que será retornanda no endpoint
        github_user_gists.append(github_temp_gist.copy())

        #Limpa o dicionário temporário utilizado para percorrer a lista retornada pela API do Git Hub
        github_temp_gist.clear()

    return jsonify(github_user_gists)


@app.route('/latestcommits', methods=['GET'])
@swag_from("swagger/latestcommits.yml")
def latestcommits():
    """
    Esse endpoint retorna os últimos commits/contribuições de um usuário do Git Hub
    em seus repositórios, em formato JSON:
    - 
    """
    
    #Recebe a informação vinda da chamada em formato .json
    content = request.json
    
    github_username = content['github_username']

    #Instância um objeto para chamada na api do Git Hub contendo as informações de usuário URL base do Git Hub
    github_request = GitHubApi(github_username, github_BASE_URL)
    
    #Recebe uma lista de dicionários de dados com as informações padrão da API do Git Hub
    #contendo as informações sobre os repositórios do usuário
    github_user_commits_default = github_request.get_github_user_commits()

    #Cria uma lista com todas as URL's de commits de cada repositório do usuário

    #github_repos_commits_urls = []
    #github_temp_gist = {}

    
    #Adiciona o gist em questão à lista que será retornanda no endpoint
    #github_user_gists.append(github_temp_gist.copy())

    #Limpa o dicionário temporário utilizado para percorrer a lista retornada pela API do Git Hub
    #github_temp_gist.clear()

    return jsonify(github_user_commits_default)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0")