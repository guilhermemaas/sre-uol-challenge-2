import requests
import logging 


class GitHubApi:
    def __init__(self, github_user: str, github_base_url: str):
        self.github_user = github_user
        self.github_base_url = github_base_url


    def get_github_user_info(self) -> dict:
        """
        Retorna todos os dados de um usuário público do Github através do endpoint /users
        """
        
        URL = f'{self.github_base_url}/users/{self.github_user}'
        
        response = requests.get(URL)
        
        return response.json()


    def get_github_user_repos(self) -> list:
        """
        Retorna todos os repositórios públicos de um usuário do Github
        """
        
        URL = f'{self.github_base_url}/users/{self.github_user}/repos'
        
        response = requests.get(URL)
        
        return response.json()


    def get_github_user_gists(self) -> list:
        """
        Retorna todos os gists públicos de um usuário do Github
        """
        
        URL = f'{self.github_base_url}/users/{self.github_user}/gists'
        
        response = requests.get(URL)
        
        return response.json()

    def get_github_user_events(self) -> list:
        """
        Retorna os últimos eventos do usuário em questão na plataforma do GitHub.
        Para filtrar as últimas contribuições/ commit, pode-se filtrar os eventos 
        "PushEvents" com commits atrelados.
        """

        URL = f'{self.github_base_url}/users/{self.github_user}/events'

        response = requests.get(URL)

        return response.json()