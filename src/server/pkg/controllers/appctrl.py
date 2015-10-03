from handler import Handler

class AppCtrl(Handler):
	def get(self):
		self.render('app.html')
