""" Copyright (C) 2015 Phil P. Ch.

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

render = web.template.render('templates/')

urls = ( 
	'/', 'index',
	'/v', 'watch_video',
	'/upload', 'upload_video',
)

class index:
	def GET(self):
		return render.index()

class watch_video:
	def GET(self):
		return "video goes here"
		#TODO

class upload_video:
	def GET(self):
		return "uploader goes here"
		#TODO
	def POST(self):
		pass
		#Video processing happens here.


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
else:
	application = web.application(urls, globals()).wsgifunc()