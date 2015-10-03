#!/usr/bin/env python
import webapp2

from pkg.controllers.transactionctrl import TransactionCtrl
from pkg.controllers.appctrl import AppCtrl
from pkg.controllers.debug import Debug

app = webapp2.WSGIApplication([
	('/transaction', TransactionCtrl),
	('/transaction/([0-9]+)', TransactionCtrl),
	('/', AppCtrl),
	('/debug', Debug)
], debug=True)
