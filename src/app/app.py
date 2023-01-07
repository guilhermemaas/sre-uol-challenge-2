import requests
import pytest 
import json
from flask import Flask, request, jsonify
from flask.wrappers import Response
import logging 
import os

class GitHubApiConsumer:
    def __init__(self, github_user: str, github_base_URL: str):
        self.github_user = github_user
        self.github_base_URL = github_base_URL

    def get_github_user_infos(self) -> dict:
        """
        """
        URL = f'{self.github_base_URL}/users/{self.github_user}'
        response = requests.get(URL)
        return response.json()

    def get_github_user_repos(self) -> list:
        """
        """
        URL = f'{self.github_base_URL}/users/{self.github_user}/repos'
        response = requests.get(URL)
        return response.json()

    def get_github_user_commits(self) -> list:
        """
        """
        URL = f'{self.github_base_URL}/users/{self.github_user}/'


"""
def main():
    github_BASE_URL = 'https://api.github.com'
    github_request = GitHubApiConsumer('guilhermemaas', github_BASE_URL)
    
    github_user_info = github_request.get_github_user_infos()
    print(github_user_info)

    github_user_repos = github_request.get_github_user_repos()
    print(json.dumps(github_user_repos, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
"""

#Endpoints

app = Flask(__name__)

github_BASE_URL = 'https://api.github.com'


@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    github_request = GitHubApiConsumer('guilhermemaas', github_BASE_URL)
    github_user_info = github_request.get_github_user_infos()

    return jsonify(github_user_info)

if __name__ == '__main__':
    app.run(host="0.0.0.0")