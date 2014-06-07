from google.appengine.ext import db
from handler import Handler
import auth
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

class FinancePage(Handler):  
    def get(self):
        transactions = db.GqlQuery("SELECT * FROM Transaction ORDER BY created DESC")
        self.render("finance.html", transactions=transactions)

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

app = webapp2.WSGIApplication([
                               ("/", Front),
                               ("/register", auth.Register),
                               ("/login", auth.Login),
                               ("/logout", auth.Logout),
                               ("/finance", FinancePage),
                               ("/addtrans", AddTrans)
], debug=True)