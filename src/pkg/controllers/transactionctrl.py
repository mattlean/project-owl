import datetime
import logging

from handler import Handler
from ..models.transactionmodel import Transaction

class TransactionCtrl(Handler):
	def get(self):
		self.response.write('Hello world!!')

	def post(self):
		cost = self.request.get('cost')
		date = self.request.get('date')

		try:
			cost = float(cost)
		except:
			self.write('cost is not float')

		self.write(str(cost) + ' ' + str(date))
		#self.write(datetime.datetime.strptime('12-01-30', '%y-%d-%m').date())
		#newTrans = Transaction(cost=cost, date=date)