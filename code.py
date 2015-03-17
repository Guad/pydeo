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
from werkzeug import secure_filename

#DATABASE SETUP
"""
database_url = environ['DATABASE_URL']
database_user = environ['DATABASE_USER']
database_pass = environ['DATABASE_PASSWORD']
database_name = environ['DATABASE_NAME']
database_method = 'postgres'
db = web.database(dburl=database_url, dbn=database_method, db=database_name)
"""
###############

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 800 * 1024 * 1024 #Set the upload limit to 800MiB

@app.route('/')
def index():
	return flask.render_template('index.html')

@app.route('/v/<videoid>')
def viewVideo():
	return flask.render_template('video.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploadVideo():
	if flask.request.method == 'GET':
		return flask.render_template('upload.html')
	else: #POST request
		return flask.render_template('upload.html')