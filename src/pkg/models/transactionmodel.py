from google.appengine.ext import db

class Transaction(db.Model):
	cost = db.FloatProperty(required = True)
	date = db.DateProperty(required = True)
	category = db.StringProperty()
	business = db.StringProperty()
	payment = db.StringProperty()
	comment = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)
