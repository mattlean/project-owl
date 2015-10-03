#!/usr/bin/env python

import webapp2

from pkg.controllers.transactionctrl import TransactionCtrl
from pkg.controllers.debug import Debug

app = webapp2.WSGIApplication([
	('/transaction', TransactionCtrl),
	('/debug', Debug)
], debug=True)
