""" Copyright (C) 2015 Guad

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""
import flask
import sha
import datetime
from werkzeug import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
from os import environ


app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 800 * 1024 * 1024 #Set the upload limit to 800MiB


######################DATABASE SETUP###############################
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db = SQLAlchemy(app)

class Video(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	description = db.Column(db.Text)
	author = db.Column(db.string, 48)
	password = db.Column(db.Text)
	date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

	def __init__(self, title, description, author, password):
		self.title = title
		self.description = description
		self.author = author
		self.password = password

	def __repr__(self):
		return '<Video %s>' % self.path
########################DB SETUP END###############################


def base36encode(number, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    """Converts an integer to a base36 string.
       We will be using this for our video ID."""
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    base36 = ''
    sign = ''
    if number < 0:
        sign = '-'
        number = -number
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36
    return sign + base36


@app.route('/')
def index():
	return flask.render_template('index.html')

@app.route('/v/<videoid>')
def viewVideo():
	video = db.query.filter_by(id=videoid).first_or_404()
	path = base36encode(video.id)
	vdata = {
			'title':video.title,
			'desc':video.description,
			'path':path,
			'author':video.author,
			'date':video.date
	}
	return flask.render_template('video.html', video=vdata)


@app.route('/upload', methods=['GET', 'POST'])
def uploadVideo():
	if flask.request.method == 'GET':
		return flask.render_template('upload.html')
	else: #POST request
		videoName = flask.request.form.get('videoName')
		videoPassword = flask.request.form.get('videoPassword')
		videoDesc = flask.request.form.get('videoDescription')
		videoFile = flask.request.files['videoFile']
		passw = sha.new(videoPassword)

		video = Video(videoName, videoDescription, 'Anonymous', passw)
		db.session.add(video)
		db.session.commit()
		vidHash = base36encode(int(video.id))

		videoOut = open('static/videos/%s.mp4' % vidHash,'wb')
		videoOut.write(videoFile)
		videoOut.close() #upload complete
		return flask.redirect(flask.url_for('index', videoid=vidHash))