# docker-puller ![License MIT](https://go-shields.herokuapp.com/license-MIT-blue.png)

[![Travis-CI Status](https://secure.travis-ci.org/glowdigitalmedia/docker-puller.png?branch=master)](http://travis-ci.org/#!/glowdigitalmedia/docker-puller)

Listen for web hooks (i.e: from docker.io builds) and run a command after that.

Introduction
============

If you use docker.io (or any similar service) to build your Docker container,
it may be possible that, once the new image is generated, you want your Docker
host to automatically pull it and restart the container.

Docker.io gives you the possibility to set a web hook after a successful build.
Basically it does a POST on a defined URL and send some informations in JSON
format.

docker-puller listen to these web hooks and can be configured to run a
particular script, given a specific hook.

Manually Test it (For developers)
=================================

Run the app.

    $ cd dockerpull
    $ ./app.py

In another terminal

    $ curl -H "Content-Type: application/json" -X \
      POST https://676b7fbc.ngrok.io/abc123/testing1 -d @hub.docker.com.test.json

note:

You can test it using [ngrok](https://ngrok.com/download).

Once you download it you can run.

    $ unzip downloaded.ngrok.zip
    $ ./ngrok http 8080

Go to your broser and test the url the shell returns you.
Which looks something like this.

https://13f008e6.ngrok.io/

Example web hook configuration
==============================

In docker.io setup a web hook with an URL like this:

https://13f008e6.ngrok.io/abc123/testing1

Example docker-puller configuration
===================================

    {
        "port": 8000,
        "token": "abc123",
        "hooks": {
            "myhook1": "commandtorun.sh"
        }
    }

Example docker container launch
===============================

(For development purpose, for production algorithm is to be run in the baremetal (for now))

    docker run -t -i --name webhook \
           -p 8000:8000 -v scripts:/root/dockerpuller/scripts
           -v config.json:/root/config.json xorilog/docker-webhook

Instructions to deploy manually with supervisor
===============================================

This is a first approach, this would be deployed with the installer itself for production environments.

    sudo apt-key -y adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" >> /etc/apt/sources.list.d/docker.list
    sudo apt-get update -y
    sudo apt-get install -y python-pip docker-engine supervisor git nginx
    sudo adduser dockeradmin (how create user with random passwords)

# Docker Puller Service.

    cd /opt
    git clone git clone https://github.com/vauxoo/docker-puller
    pip install -r requirements.txt

# Add a chain to the config.json

    +    "token": "TESTCHAIN_ALEATORY_JUST_CREATE_ONE_FOR_YOU",

# Configure Supervisord (commands as root)

    echo "[program:dockerpuller]
    directory=/opt/docker-puller/dockerpuller/
    command=/opt/docker-puller/dockerpuller/app.py
    " > /etc/supervisor/conf.d/dockerpuller.conf

# Now restart supervisor

    service supervisor restart
    
# Test What you did.

Go to ip.server.service.running:8080 and you should see the daemon telling you 
the servide working.

# Mainteinance instructions.

Change version after a release:

    bumpversion patch

test:

    TODO.

Packetize alá python.

    TODO.

