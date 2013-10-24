# Server config

## Create server user


## Configure ssh

### Keys
### Local ssh config


## Basic software

    apt-get install vim
    apt-get install git


## Python package dependencies

### Pillow

    apt-get install libjpeg62-dev libjpeg62


## Python 

### pip

    apt-get install python-pip

### virtualenv

    apt-get install python-virtualenv

### virtualenvwrapper

    pip install virtualenvwrapper


## Node

    apt-get install nodejs
    cd /usr/bin
    ln -s nodejs node

### npm

    apt-get install npm

### requirejs

    npm install -g requirejs


## MySQL

### Create user with appropriate privileges


## SMTP

### postfix

https://help.ubuntu.com/community/Postfix

### Add user with authentication

http://postfix.state-of-mind.de/patrick.koetter/smtpauth/smtp_auth_mailservers.html


## Webapp
### Clone
### Environment variables for settings


## memcached


## nginx
### /static/
### /media/
### /
https://www.digitalocean.com/community/articles/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn

## Supervisor

http://www.edvanbeinum.com/how-to-install-and-configure-supervisord
http://supervisord.org/configuration.html


## Gunicorn


## Swap space

http://dorwardvillaruz.com/lamp-digitalocean-5-droplets/

dd if=/dev/zero of=/swapfile bs=1024 count=1048576
mkswap /swapfile
swapon /swapfile
free -m
echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
