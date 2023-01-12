# sre-uol-challenge-2
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/gmaas-github-api)](https://artifacthub.io/packages/search?repo=gmaas-github-api)

## Sobre:

Uma API desenvolvida em Python/Flask e tem como objetivo extrair algumas informações úteis de um usuário da API pública do GitHub.

Links importantes:

[Helm chart no Artifact Hub](https://artifacthub.io/packages/helm/gmaas-github-api/gmaas-github-api?modal=install)

[Imagem Docker no Docker Hub](https://hub.docker.com/r/gmaas2/github-api/tags)

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

Pipeline:

Para o build da Imagem Docker

Documentação:

Desenvolvimento:

Monitoramento:

To-do: