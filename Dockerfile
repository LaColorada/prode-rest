# pull the official base image
FROM python:3.8-slim-bullseye

RUN useradd -ms /bin/bash lacolorada

# set work directory
RUN mkdir /app
ADD requirements.txt /app
WORKDIR /app

# set environment variables
# PIP_DISABLE_PIP_VERSION_CHECK disables an automatic check for pip updates each time
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# PYTHONDONTWRITEBYTECODE means Python will not try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED ensures our console output is not buffered by Docker
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $PYTHONPATH:/app

# install dependencies
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

STOPSIGNAL SIGHUP

# Copy all code files into image. Uncomment for production
ADD . /app

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD su lacolorada -c 'python3 manage.py runserver 0.0.0.0:8000'
# CMD su 'python3 manage.py runserver 0.0.0.0:8000'
