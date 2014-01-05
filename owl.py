import os
import webapp2
import jinja2

from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
JINJA_ENV = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = JINJA_ENV.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

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
        
app = webapp2.WSGIApplication([("/finance", FinancePage),
                               ("/addtrans", AddTrans)], debug=True)