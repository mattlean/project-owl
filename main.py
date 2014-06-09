from google.appengine.ext import db
from handler import Handler
import auth
import json
import logging
import webapp2

class Front(Handler):
    def get(self):
        self.redirect("/finance")

class Transaction(db.Model):
    date = db.StringProperty(required = True) #should really be stored as DateProperty
    description = db.StringProperty()
    business = db.StringProperty()
    category = db.StringProperty()
    transType = db.StringProperty()
    amount = db.FloatProperty(required = True) #need to cover case where user doesn't input a valid float
    created = db.DateTimeProperty(auto_now_add = True)
    
    def as_dict(self):
        datadict = {"date": self.date,
             "description": self.description,
             "business": self.business,
             "category": self.category,
             "transType": self.transType,
             "amount": self.amount}
        return datadict

class FinancePage(Handler):
    def render_json(self, datadict):
        json_dump = json.dumps(datadict)
        json_txt = '{"items": ' + json_dump + '}'
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)
    
    def get(self):
        transactions = db.GqlQuery("SELECT * FROM Transaction ORDER BY created DESC")
        transactions = list(transactions)
        if self.format == "html":
            self.render("finance.html", transactions=transactions)
        else:
            return self.render_json([transaction.as_dict() for transaction in transactions])

class AddTrans(Handler):
    def get(self):
        self.render("addtrans.html")
        
    def post(self):
        date = self.request.get("date")
        description = self.request.get("description")
        business = self.request.get("business")
        category = self.request.get("category")
        transType = self.request.get("transType")
        amount = float(self.request.get("amount"))
        
        if date and amount:
            newTransaction = Transaction(date=date, description=description, business=business, category=category, transType=transType, amount=amount)
            newTransaction.put()            
            self.redirect("/finance")
        else:
            error = "You must input at least a date and amount!"
            self.render("addtrans.html", date=date, description=description, business=business, category=category, transType=transType, amount=amount, error=error)

class AndroidFinanceHandler(webapp2.RequestHandler):
    def get(self):
        date = self.request.get("date")
        description = self.request.get("description")
        business = self.request.get("business")
        category = self.request.get("category")
        transType = self.request.get("transType")
        amount = self.request.get("amount")
        
        if (date == "") or (amount == ""):
            logging.error("Android submission: Date or amount missing!")
        else:
            isNotFloat = False

            try:
                float(amount)
            except ValueError:
                logging.error("Android submission: Amount is not a valid float!")
                isNotFloat = True
                
            if isNotFloat == False:
                amount = float(amount)
                newTransaction = Transaction(date=date, description=description, business=business, category=category, transType=transType, amount=amount)
                newTransaction.put()
                logging.debug("Android submission: Submission succesful!")

app = webapp2.WSGIApplication([
                               ("/?", Front),
                               ("/register/?", auth.Register),
                               ("/login/?", auth.Login),
                               ("/logout/?", auth.Logout),
                               ("/finance/?(?:\.json)?", FinancePage),
                               ("/finance/addtrans/?", AddTrans),
                               ("/finance/android/submit", AndroidFinanceHandler)
], debug=True)