import logging

from handler import Handler

class TransactionCtrl(Handler):
	def get(self):
		self.response.write('Hello world!!')

	def post(self):
		logging.info('post request got')