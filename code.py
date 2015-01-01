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
import web
from os import environ


render = web.template.render('templates/')

#DATABASE SETUP
database_url = environ['DATABASE_URL']
database_user = environ['DATABASE_USER']
database_pass = environ['DATABASE_PASSWORD']
database_name = environ['DATABASE_NAME']
database_method = 'postgres'

db = web.database(dburl=database_url, dbn=database_method, user=database_user, pw=database_pass, db=database_name)
###############

urls = ( 
	'/', 'index',
	'/v', 'watch_video',
	'/upload', 'upload_video',
)
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

class index:
	def GET(self):
		return render.index()

class watch_video:
	def GET(self):
		input = web.input(id=None)
		#Sanitize input here and get data about the video
		return render.video(str(input.id))

class upload_video:
	def GET(self):
		return render.upload()
	def POST(self):
		x = web.input(videoFile={}) #x is out input basket
		filedir = "videos"
		if 'videoFile' in x:
			q = db.insert('videos', title=x.videoName, date=SQLLiteral('NOW()'), password=x.videoPassword, description=x.videoDescription, views=0, likes=0, dislikes=0)
			"""
			NOTICE
			THE PASSWORD WILL BE ENCRYPTED, THIS IS TEMPORAL

			q RETURNS THE ID
			"""
			videoOut = open(filedir +'/'+ base36encode(int(q)) + '.mp4','wb')
			videoOut.write(x.videoFile.file.read())
			videoOut.close() #upload complete
        	raise web.seeother('/v?id=' + base36encode(int(q)))

		#Video processing happens here.


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
else:
	application = web.application(urls, globals()).wsgifunc()