from handler import Handler

class Debug(Handler):
	def get(self):
		self.render('debug.html')
