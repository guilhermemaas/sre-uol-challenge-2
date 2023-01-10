FROM python:3.10-slim-buster

ENV APP_HOME=/home/app

#Cria o diretório para o usuário app
RUN mkdir -p /home/app/api

#Cria o usuário app
RUN groupadd app && useradd -g app app

#Cria o diretório home do usuário app
RUN mkdir -p $APP_HOME

#Seta o diretório de trabalho
WORKDIR $APP_HOME

#Copia e instala os requisitos da app Flask
COPY . .
RUN python -m pip install -r requirements.txt

#Altera o owner dos arquivos da aplicação
RUN chown -R app:app $APP_HOME
USER app

#Expõe a porta 5000 no container
EXPOSE 5000

#Executa o aplicação através do Gunicorn
CMD ["gunicorn", "--workers=1", "--bind", "0.0.0.0:5000", "--log-level=info", "app:app"]