#!/bin/bash

docker stop flask
docker rm flask
docker image rm flask-yt
docker build --tag flask-yt .
docker run -d --name flask --mount type=bind,source=/mnt/drive/stuff/Music,target=/flaskYoutubeDownloader/downloads --mount type=bind,source=/home/till/flaskYT/data,target=/flaskYoutubeDownloader/instance -p 5000:5000 flask-yt:latest
