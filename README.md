# project

## Getting Started


Make sure you have install Docker
https://docs.docker.com/compose/install/

and Docker-Compose
```
curl -L https://github.com/docker/compose/releases/download/1.12.0-rc2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

First you have to buil the containers for the first time
`docker-compose build web`

Now you have to up the containers
`docker-compose up -d`

Docker will give you the follow comand
`docker volume create --name=db_data`

Check the logs with
`docker-compose logs`

Run django for the first time
`docker-compose run web python manage.py makemigrations`

`docker-compose run web python manage.py migrate`

`docker-compose run web python manage.py createsuperuser`
