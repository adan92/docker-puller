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

## Install flask

```
$ pip install flask
Collecting flask
  Downloading Flask-0.11-py2.py3-none-any.whl (80kB)
```

## Run the app.

```
$ cd dockerpull
$ ./app.py
```

## Post to Webhook

Make sure you are in the directory of the app.py and that you see the file `hub.docker.com.test.json`.

```
$ curl -H "Content-Type: application/json" -X POST http://localhost/abc123/testing1 -d @hub.docker.com.test.json
```

## Post through ngrok

You can test it using [ngrok](https://ngrok.com/download).

Once you download it you can run.

```
$ unzip downloaded.ngrok.zip
$ ./ngrok http 8080
ngrok by @inconshreveable                                (Ctrl+C to quit)

Tunnel Status                 online
Version                       2.0.25/2.1.1
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://7181fbfd.ngrok.io -> localhost:8080
Forwarding                    https://7181fbfd.ngrok.io -> localhost:8080
```

Then, you can make calls locally:

```
$ curl -H "Content-Type: application/json" -X \
  POST https://7181fbfd.ngrok.io/abc123/testing1 -d @hub.docker.com.test.json
```

## Logs from app.py

The output of the execution of the app displays the webhook calls.

```
$ ./app.py
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
received {"push_data": {"pushed_at": 1460855619, "images": [], "tag": "latest", "pusher": "vauxoo"}, 
"callback_url": "https://registry.hub.docker.com/u/vauxoo/urlshortener/hook/2cdf030jcie544fhee1342gg0352b12gd/",
"repository": {"status": "Active", "description": "vx.hg served services.", "is_trusted": true, 
"full_description": "# urlshortener\nA URL shortening Flask micro website similar to bit.ly \n\nTo launch the 
application:\n\n    docker build -t urlshortener .\n    docker run -ti -p 5000:5000 
-v /tmp/var:/app/var urlshortener\n\nTo program on it:\n\n    virtualen -p python3 env\n    . 
env/bin/activate\n    pip install -r requirements.txt\n", "repo_url": "https://hub.docker.com/r/vauxoo/urlshortener",
"owner": "vauxoo", "is_official": false, "is_private": false, "name": "urlshortener", "namespace": "vauxoo", 
"star_count": 0, "comment_count": 0, "date_created": 1460839654, 
"dockerfile": "FROM python:3.4\nMAINTAINER Vincent Fretin <vincentfretin@ecreall.com>\n\nRUN mkdir -p /app/var\nCOPY
 . /app/\nRUN addgroup --quiet --gid \"1000\" \"u1000\" && \\\n    adduser \\\n        --shell /bin/bash \\\n    
--disabled-password \\\n        --force-badname \\\n        --no-create-home \\\n        --uid \"1000\" \\\n
        --gid \"1000\" \\\n        --gecos '' \\\n        --quiet \\\n        --home \"/app\" \\\n
        \"u1000\"\nWORKDIR /app\nRUN pip install -r requirements.txt\nRUN chown -R u1000:u1000 
/app\nUSER u1000\n\nEXPOSE 5000\nVOLUME /app/var\n\nCMD [\"python\", \"main.py\"]\n", 
"repo_name": "vauxoo/urlshortener"}}
127.0.0.1 - - [02/Jun/2016 22:46:08] "POST /abc123/testing1 HTTP/1.1" 200 -
```

## Logs from the Webhook Handler

The logs are created at dockerpuller/scripts/logs/testing.log. You can initially touch the file and tail it.

```
$ touch dockerpuller/scripts/logs/testing.log
$ tail -f dockerpuller/scripts/logs/testing.log
[02/06/16 23:09:39] 127.0.0.1
[02/06/16 23:10:02] 127.0.0.1
```

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

