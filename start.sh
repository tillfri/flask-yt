#!/bin/bash
# start container on VM
# docker run -d --name flask --mount type=bind,source=/home/till/PycharmProjects/flaskProject/downloads,target=/flaskYoutubeDownloader/downloads -p 5000:5000 flask-ytdownloader:latest

# start container on PI
# docker run -d --name flask --mount type=bind,source=/mnt/drive/stuff/Music,target=/flaskYoutubeDownloader/downloads --mount type=bind,source=/home/till/flaskProject/data,target=/flaskYoutubeDownloader/instance -p 5000:5000 flask-ytdownloader:latest



