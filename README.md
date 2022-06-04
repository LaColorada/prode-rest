# Prode REST API

An API project using [Django REST Framework](https://www.django-rest-framework.org/) about a prode/sports lottery that lets users compete in a friendly app with sports results and keep track of the scores, main player, pichichi and many more.

Still in construction.

## Features

Results prediction app

Score rank

Set up sport/league

Custom users app

## What's missing

...

## FAQs

Q: Can i use the project for personal/commercial use?

A: Yes.

## Getting started

How to section with the steps to set up the project in your system.

Docker?

Ubuntu?

### Download the code

To download the code, the best thing to do is to `fork` this project to your personal account by clicking on [this link](https://github.com/gotoiot/service-django-rest-api/fork). Once you have the fork in your account, download it from the terminal with this command (remember to put your username in the link):

```
git clone https://github.com/USER/django-rest-api.git
```

> In case you don't have a Github account, or you don't want to fork, you can directly clone this repo with the command `git clone https://github.com/gotoiot/service-django-rest-api.git`.

## Documentation

### Dir Structure

Folder structure for scalability. General folder contains:

```sh
├── [other files/folders]       # files/folders arount the Django project 
├── [project-root-folder]       # the root folder containing the Django app
|   ├── core                    # the main Django app folder
│   │   ├── commands            # commands executed by the Django shell 
│   │   ├── settings            # the folder to store different settings
│   │   |   └── settings.py
│   │   ├── tests               # package to store tests in an scalable way
│   │   |   ├── tests.py
|   │   │   |   ├── __init__.py 
|   │   │   |   └── tests.py 
│   │   ├── __init__.py 
│   │   ├── admin.py            # base logic related to admin classes
│   │   ├── asgi.py             # autogenerated
│   │   ├── auth.py             # logic related to identify the current user
│   │   ├── models.py           # base logic related to models
│   │   ├── pagination.py       # configurations about pagination 
│   │   ├── permissions.py      # the main permissions the project has
│   │   ├── urls.py             # main project url configurations
│   │   ├── utils.py            # module to support common things at project level
│   │   ├── validators.py       # logic related to validation at project level
│   │   ├── views.py            # views related to the project, not to applications
│   │   └── wsgi.py             # autogenerated
|   ├── [apps]                  # the django applications
|   |   ├── [prode]             # prode app folder
│   │   └── [users]             # users app folder
|   ├── [integrations]          # integrations with third party services
|   ├── [templates]             # all the project templates should be in this dir
|   └── manage.py               # module to manage the project and common operations
```

Application folder structure:

```sh
├── application
│   ├── migrations          
│   ├── models              # package to store models separatelu
│   │   ├── __init__.py
│   │   └── model.py
│   ├── tests               # package to store tests separately
│   │   ├── __init__.py
│   │   └── tests.py
│   ├── __init__.py         # autogenerated
│   ├── admin.py            # admin class definition and configuration
│   ├── apps.py             # required by Django
│   ├── filters.py          # logic related to filter
│   ├── permissions.py      # application level permissions
│   ├── serializers.py      # application level serializers
│   ├── services.py         # logic related to the flows on the application
│   ├── urls.py             # application level url configuration
│   └── views.py            # views
```


## Used technologies 🛠️

In this section you can see the most important technologies used.

<details><summary><b>See the complete list of technologies</b></summary><br>

* [Docker](https://www.docker.com/) - Ecosystem that allows the execution of software containers.
* [Docker Compose](https://docs.docker.com/compose/) - Tool that allows managing multiple Docker containers.
* [Python](https://www.python.org/) - Language in which the services are made.
* [Django](https://www.djangoproject.com/) - Popular Python framework for web application development.
* [Django REST Framework](https://www.django-rest-framework.org/) - Django-based framework for designing REST APIs.
* [PostgreSQL](https://www.postgresql.org/) - Database to query and store data.
* [Visual Studio Code](https://code.visualstudio.com/) - Popular multi-platform development IDE.

</details>

## About LaColorada 

LaColorada is a Argentinian-based startup dedicated to build backend services for enterprises and different projects.