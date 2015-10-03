import json
from datetime import datetime
from google.appengine.ext import db

from handler import Handler
from ..models.transactionmodel import Transaction

class TransactionCtrl(Handler):
	def get(self, transId=''):
		try:
			key = db.Key.from_path('Transaction', int(transId))
			trans = db.get(key)

			if not trans:
				raise ValueError('Transaction does not exist')

			transDict = {
							'cost': trans.cost,
							'date': trans.date.strftime('%Y-%m-%d'),
							'category': trans.category,
							'business': trans.business,
							'payment': trans.payment,
							'comment': trans.comment
						}

			self.write(json.dumps(transDict))
		except:
			self.write('')

	def post(self):
		cost = self.request.get('cost')
		date = self.request.get('date')
		category = self.request.get('category')
		business = self.request.get('business')
		payment = self.request.get('payment')
		comment = self.request.get('comment')

		try:
			cost = float(cost)
		except:
			self.write('')
			return

		try:
			date = datetime.strptime(date, '%Y-%m-%d').date()
		except:
			self.write('')
			return

		newTrans = Transaction(cost=cost, date=date, category=category, business=business, payment=payment, comment=comment)
		newTrans.put()
