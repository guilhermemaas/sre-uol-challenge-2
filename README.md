# sre-uol-challenge-2
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/gmaas-github-api)](https://artifacthub.io/packages/search?repo=gmaas-github-api)

## Sobre:

Uma API desenvolvida em Python/Flask e tem como objetivo extrair algumas informações úteis de um usuário da API pública do GitHub.

Links importantes:

[Helm chart no Artifact Hub](https://artifacthub.io/packages/helm/gmaas-github-api/gmaas-github-api?modal=install)

[Imagem Docker no Docker Hub](https://hub.docker.com/r/gmaas2/github-api/tags)

<br>

## Instalando e rodando a aplicação:
### Helm:

Adicione o repositório:

`helm repo add gmaas-github-api https://guilhermemaas.github.io/gmaas-github-api/charts`

Instale o chart:

`helm install my-gmaas-github-api gmaas-github-api/gmaas-github-api --version 1.0.16`

Acessando a aplicação localmente:

`kubectl port-forward svc/my-gmaas-github-api 5000:5000`

A aplicação estará disponível localmente na porta 5000. Você pode começar acessando a página de documentação(swagger) e fazer alguns testes para entender como a API funciona:

http://localhost:5000/apidocs

Na raíz do projeto existe um arquivo contendo uma collection do Insomnia com exemplos de cada endpoint.

Caso queira desinstalar:
`helm uninstall my-gmaas-github-api`

### Docker:

Clone o repositório:

`git clone https://github.com/guilhermemaas/sre-uol-challenge-2.git`

Utilize o docker-compose para subir a aplicação:

`cd sre-uol-challenge-2.git && docker-compose up -d`

Da mesma maneira, a aplicação estará disponível localmente na porta 5000, e a documentação nesta url http://localhost:5000/apidocs.

Caso queira desinstalar:

`docker-compose down`

<br>

## Documentação:

Swagger: http://localhost:5000/apidocs

<div>
    <img src="doc/img/swagger.png">
<div>


Insomnia:
<div>
    <img src="doc/img/insomnia.png">
<div>

Detalhes sobre os métodos da API:

| Método HTTP | Endpoint | Descrição | Informações retornadas |
| ----------- | ----------- | ----------- | ----------- |
| GET | /user/{username}/info | Retorna um resumo de informações referentes a um usuário do GitHub | Login do usuário, Nome do usuário, E-mail do usuário, Bio, URL para o avatar do usuário, Quantidade de repositórios públicos, Quantidade de gists públicos, Quantidade de usuários seguidores, Quantidade de usuários que está seguindo, Data de criação da conta |
| GET | /user/{username}/repos | etorna informações referentes aos repositórios públicos de um usuário do GitHub |  Nome do repositório, ID do repositório, Nome completo do repositório, Descrição do repositório, Login do owner/dono do repositório, URL git do repositório, URL ssh do repositório, URL com listagem de commits no repositório, Data de criação, Último push/alteração, Branch default/padrão, Número de Issues em aberto |
| GET | /user/{username}/gists | Retorna informações referentes aos gists de um usuário do GitHub |  ID do gist, URL do gist, Arquivo(s), Owner/Dono do gist, Data/Hora de criação, Data/Hora de última atualização |
| GET | /user/{username}/commits | Retorna informações referentes aos últimos commits/contribuições de um usuário no GitHub |  ID do evento, ID do repositório, Nome do repositório, URL do repositório, URL do commit, Mensagem do commit, Autor do commit, Data/Hora do Push |


<br>

## Pipeline:

O build da aplicação ocorre de forma automática através do GitHub Actions toda vez que um novo código é adicionado. Os detalhes dos últimos builds podem ser visualizados neste [link](https://github.com/guilhermemaas/sre-uol-challenge-2/actions). 

<div>
    <img src="doc/img/github_actions.png">
<div>

Caminho do arquivo .yaml da pipeline: 
.github/workflows/main.yml

Desenvolvimento:

Monitoramento:

To-do: