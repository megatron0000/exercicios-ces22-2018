import os

from flask import Flask, request, render_template, session, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, patch_request_class, configure_uploads
from sqlalchemy import Column, Text

app = Flask(__name__)
app.secret_key = 'Som$R@ndom $trIng H$r$'
patch_request_class(app)
app.config['UPLOADS_DEFAULT_DEST'] = './uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Photo(db.Model):
    name = Column(Text, primary_key=True)
    username = Column(Text)


class User(db.Model):
    username = Column(Text, primary_key=True)


photos = UploadSet('photos', IMAGES)

configure_uploads(app, (photos,))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        username = session['username']
    except KeyError:
        return redirect(url_for('login') + '?forced=true')
    if request.method == 'POST':
        if 'photo' not in request.files:
            return render_template('upload.html', error='Must submit a file')
        try:
            filename = photos.save(request.files['photo'])
            rec = Photo(name=filename, username=username)
            db.session.add(rec)
            db.session.commit()
            return render_template('upload.html', success='Photo saved')
        except:
            return render_template('upload.html', error='Error saving file. Is it an image ?')
    return render_template('upload.html')


@app.route('/')
def index():
    try:
        username = session['username']
    except KeyError:
        return redirect(url_for('login') + '?forced=true')
    nameurls = [
        ({
            'url': photos.url(photo.name),
            'name': photo.name
        })
        for photo in Photo.query.filter_by(username=username).all()
    ]
    return render_template(
        'list.html',
        photonameurls=nameurls,
        nophoto=len(nameurls) == 0,
        username=username
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            forced = True if request.args['forced'] == 'true' else False
        except KeyError:
            forced = False
        return render_template('login.html', forced=forced)
    if request.method == 'POST':
        session['username'] = request.form['username']

        # Redirect
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', request.form['username'])
        return resp


@app.route('/logout')
def logout():
    was_logged_in = True
    try:
        del session['username']
    except KeyError:
        was_logged_in = False
    return render_template('logged_out.html', was_logged_in=was_logged_in)


if __name__ == '__main__':
    db.create_all()
    app.run('127.0.0.1', os.environ.get('PORT', '8000'), debug=True)
