#!/bin/bash
echo "Building and restarting"
# Image name should be from parameter $1
docker pull vauxoo/urlshortener
echo "Stoping If exists"
docker stop urlshortener
docker rm urlshortener
echo "Running"
docker run -e "SHORTENER_DOMAIN=vx.ht" -di --name urlshortener -p 5000:5000 -v var:/app/var vauxoo/urlshortener:latest
