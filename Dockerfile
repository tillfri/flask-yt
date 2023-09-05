FROM python:3.11.4-slim-bullseye

WORKDIR /flaskYoutubeDownloader

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]