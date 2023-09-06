import os
import logging
import pytube.exceptions
from flask import Flask, render_template, url_for, request, redirect
from pytube import YouTube
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
db = SQLAlchemy(app)
# adjust path depending on OS/pythonInterpreter
output_folder = "downloads"  # "/flaskYoutubeDownloader/downloads"
logging.basicConfig(level=logging.INFO)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Task %r>' % self.id


# with app.app_context():
#    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        yt_url = request.form['content']
        return download_video(yt_url)
    else:
        history = Video.query.order_by(Video.date_created).all()
        return render_template('index.html', history=history)


@app.route('/delete/<int:id>')
def delete(id):
    video_to_delete = Video.query.get_or_404(id)

    try:
        db.session.delete(video_to_delete)
        db.session.commit()

        # delete .mp3 file on drive
        path = os.path.join(output_folder, video_to_delete.path)
        if os.path.isfile(path):
            os.remove(path=path)
        return redirect('/')
    except:
        return "Something went wrong deleting the entry in the database"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    video = Video.query.get_or_404(id)
    old_path = os.path.join(output_folder, video.path)

    if request.method == 'POST':
        video.path = request.form['path'] + ".mp3"
        video.content = request.form['path']

        try:
            db.session.commit()
            path = os.path.join(output_folder, video.path)
            if os.path.isfile(old_path):
                os.rename(old_path, path)
            return redirect('/')
        except:
            return 'Something went wrong trying to update the entry in the database'
    else:
        return render_template('update.html', video=video)


def download_video(url: str):
    try:
        yt = YouTube(url, use_oauth=False)
        logging.info(yt.title)
        stream = yt.streams.get_audio_only()

        title = cleanup_title(yt.title)
        logging.info(title)
        filename = title + ".mp3"
        stream.download(output_path=output_folder, filename=filename)
        new_file = Video(content=title, path=filename)
        db.session.add(new_file)
        db.session.commit()

        return redirect('/')
    except pytube.exceptions.RegexMatchError:
        return render_template('ErrorRegexMatch.html')
    except pytube.exceptions.AgeRestrictedError:
        return render_template('ErrorAgeRestricted.html')
    except:
        return 'Something went wrong while trying to download the video'


def cleanup_title(og_title: str):
    """
    Remove chars from YouTube video title in order to maintain allowed title name for Windows
    :param og_title:
    :return:
    """
    translation_table = str.maketrans('', '', '<>:/|?*')

    # Remove characters from the string
    input_string = og_title
    result_string = input_string.translate(translation_table)
    return result_string


if __name__ == '__main__':
    app.run()
