#!/usr/bin/env python

import webapp2

from controllers.transactionctrl import TransactionCtrl
from controllers.debug import Debug

app = webapp2.WSGIApplication([
	('/transaction', TransactionCtrl),
	('/debug', Debug)
], debug=True)
