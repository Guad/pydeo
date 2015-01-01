import web
import urllib2

render = web.template.render('templates/')

urls = ( 
	'/', 'index',
)

class index:
	def GET(self):
		return "It works!"

		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
else:
	application = web.application(urls, globals()).wsgifunc()