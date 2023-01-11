import requests
from flask import Flask, jsonify, render_template, abort, json
from prometheus_flask_exporter import PrometheusMetrics
from operator import itemgetter
import logging 
import os
from datetime import date
from flasgger import Swagger
from flasgger.utils import swag_from
from werkzeug.exceptions import HTTPException
from domain.github import GitHubApi


app = Flask(__name__)

#Gera o endpoint /metrics utilizando o Flask Prometheus Exporter
metrics = PrometheusMetrics(app)

#Gera a documentação com Swagger utilizando o Flasgger
swagger = Swagger(app)

github_base_url = 'https://api.github.com'

#To-do: Instanciando variáveis com variáveis de ambiente (Jaeger, Log Level, etc).
JAEGER_HOST = os.getenv('JAGER_HOST')
JAEGER_PORT = os.getenv('JAEGER_PORT')
JAEGER_SERVICE_NAME = os.getenv('github-api')

GITHUB_API_ENV = os.getenv('GITHUB_API_ENV') #dev/prod
GITHUB_API_LOG_LEVEL = os.getenv('GITHUB_API_LOG_LEVEL') #DEBUG, INFO, WARNING, ERROR, CRITICAL, INFO


#Definição de log level conforme ambiente (dev/prod)
if GITHUB_API_ENV == 'dev' or GITHUB_API_LOG_LEVEL == 'DEBUG':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
elif GITHUB_API_ENV == 'prod' or GITHUB_API_LOG_LEVEL == 'WARNING':
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
elif GITHUB_API_LOG_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'INFO']:
    logging.basicConfig(level=GITHUB_API_LOG_LEVEL, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
else:
    app.logger.info('Nenhum nível de log foi declarado em variáveis de ambiente. Será ignorado.')


@app.errorhandler(HTTPException)
def handle_exception(error):
    """
    Retorna um JSON contendo um tratamento e descrição do item.
    """
    response = error.get_response()

    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    response.content_type = "application/json"
    
    return response


app.logger.info('SRE UOL Challenge 2: API GitHub')


@app.route('/')
@app.route('/home')
@app.route('/index')
@app.route('/entry')
def index():
    """
    Página default ao chamar URL's "raíz"
    """

    return render_template('index.html',
        the_tittle=f'SRE UOL Challenge 2: API GitHub - Data: {date.isoformat(date.today())}')


@app.route('/health')
def health():
    """
    A API do GitHub estar disponível/respondendo é imprescindível para o funcionamento da
    aplicação, desta maneira, será realizado um teste de chamada para identificar o 
    seu funcionamento
    """
    github_base_url = 'https://api.github.com'
    URL = f'{github_base_url}/users/github'
    
    try:
        response = requests.get(URL)
    except Exception as err:
        app.logger.error(str(err))
    
    if response.status_code == 200:
        return 'Healthy'
    else:
        return 'Unhealthy'


@app.route('/read')
def read():
    """
    Endpoint retorna o status que a aplicação está disponível para requests
    """
    return 'Ready'


@app.route('/user/<username>/info', methods=['GET'])
@swag_from("swagger/userinfo.yml")
def userinfo(username):
    """
    Esse endpoint retorna os seguintes dados de um usuário do GitHub, em formato JSON:
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

    github_username = username

    #Instância um objeto para chamada na api do GitHub contendo as informações de usuário URL base do GitHub
    github_request = GitHubApi(github_username, github_base_url)
    
    logging.info(f'Buscando dados de perfil do usuário {github_username}.')

    #Recebe um dicionário de dados com as informações padrão da API do GitHub (/users)
    try:
        github_user_info_default = github_request.get_github_user_info()
    except Exception as err:
        app.logger.error(str(err))

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
    
    return jsonify(github_user_info)


@app.route('/user/<username>/repos', methods=['GET'])
@swag_from("swagger/userrepos.yml")
def userrepos(username):
    """
    Esse endpoint retorna os seguintes dados referentes aos repositórios de um
    usuário do GitHub, em formato JSON:
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

    #Instância um objeto para chamada na api do GitHub contendo as informações de usuário URL base do GitHub
    github_request = GitHubApi(github_username, github_base_url)
    
    logging.info(f'Buscando repositórios públicos do usuário {github_username}.')

    #Recebe um dicionário de dados com as informações padrão da API do GitHub (/users)
    try:
        github_user_repos_default = github_request.get_github_user_repos()
    except Exception as err:
        app.logger.error(str(err))

    github_user_repos = []
    github_temp_repo = {}

    #Percore a lista de repositórios retornado pela API do GitHub adicionando a um dicionário temporário os 
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

        #Limpa o dicionário temporário utilizado para percorrer a lista retornada pela API do GitHub
        github_temp_repo.clear()

    #Ordena a lista em ordem alfabética para apresentação
    github_user_repos = sorted(github_user_repos, key=itemgetter('name'), reverse=False)

    #Retorna as informações dos campos citados acima
    return jsonify(github_user_repos)


@app.route('/user/<username>/gists', methods=['GET'])
@swag_from("swagger/usergists.yml")
def usergists(username):
    """
    Esse endpoint retorna os seguintes dados referentes aos gists de um
    usuário do GitHub, em formato JSON:
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

    #Instância um objeto para chamada na api do GitHub contendo as informações de usuário URL base do GitHub
    github_request = GitHubApi(github_username, github_base_url)
    
    logging.info(f'Buscando gists públicos do usuário {github_username}.')

    #Recebe um dicionário de dados com as informações padrão da API do GitHub (/users)
    try:
        github_user_gists_default = github_request.get_github_user_gists()
    except Exception as err:
        app.logger.error(str(err))
    
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

        #Limpa o dicionário temporário utilizado para percorrer a lista retornada pela API do GitHub
        github_temp_gist.clear()

    return jsonify(github_user_gists)


@app.route('/user/<username>/commits', methods=['GET'])
@swag_from("swagger/usercommits.yml")
def usercommits(username):
    """
    Esse endpoint retorna os seguintes dados referentes aos últimos commits de um
    usuário do GitHub, através do endpoint de eventos em formato JSON:
    - ID do evento
    - ID do repositório
    - Nome do repositório
    - URL do repositório
    - URL do commit
    - Mensagem do commit
    - Autor do commit
    - Data/Hora do Push
    """
    
    #Recebe a informação vinda da chamada em formato .json

    github_username = username

    #Instância um objeto para chamada na api do GitHub contendo as informações de usuário URL base do GitHub
    github_request = GitHubApi(github_username, github_base_url)
    
    logging.info(f'Buscando últimos commits/contribuições do usuário {github_username}.')

    #Recebe um dicionário de dados com as informações padrão da API do GitHub (/users/username/events)
    try:
        github_user_events_default = github_request.get_github_user_events()
    except Exception as err:
        app.logger.error(str(err))

    #Ajusta um dicionário temporário somente os campos que queremos retornar na API e eventos do tipo
    #"PushEvent" para buscar os últimos commits
    github_user_commits = []
    github_temp_event = {}

    for event in github_user_events_default:

        if event['type'] == "PushEvent":
            github_temp_event = {
                'id': event['id'],
                'repo_id': event['repo']['id'],
                'repo_name': event['repo']['name'],
                'repo_url': event['repo']['url'],
                'commits_details': event['payload']['commits'],
                'push_date': event['created_at'],
            }
            #Adiciona o gist em questão à lista que será retornanda no endpoint
            github_user_commits.append(github_temp_event.copy())

            #Limpa o dicionário temporário utilizado para percorrer a lista retornada pela API do GitHub
            github_temp_event.clear()

        else:
            pass

    return jsonify(github_user_commits)
    

if __name__ == '__main__':
    #app.run(host="0.0.0.0")
    app.run()