from datetime import datetime

from handler import Handler
from ..models.transactionmodel import Transaction

class TransactionCtrl(Handler):
	def get(self):
		self.response.write('Hello world!!')

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
			self.write('cost is not float')
			return

		try:
			date = datetime.strptime(date, '%Y-%m-%d').date()
		except:
			self.write('date is in improper format: ' + date)
			return

		newTrans = Transaction(cost=cost, date=date, category=category, business=business, payment=payment, comment=comment)
		newTrans.put()
