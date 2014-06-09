from google.appengine.ext import db
from string import letters
import hashlib
import hmac
import jinja2
import os
import random
import webapp2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
JINJA_ENV = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape = True)
secret = "iTsAsEcReTtOeVeRyBoDy1986"

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()
    
    @classmethod
    def make_salt(cls, length = 5):
        return ''.join(random.choice(letters) for x in xrange(length))
    
    @classmethod
    def make_pw_hash(cls, name, pw, salt = None):
        if not salt:
            salt = cls.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return "%s,%s" % (salt, h)
    
    @classmethod
    def valid_pw(cls, name, password, h):
        salt = h.split(',')[0]
        return h == cls.make_pw_hash(name, password, salt)
    
    @classmethod
    def by_id(cls, userid):
        return cls.get_by_id(userid)
    
    @classmethod
    def by_name(cls, name):
        user = cls.all().filter("name =", name).get()
        return user

    @classmethod
    def create_user(cls, name, pw, email = None):
        pw_hash = cls.make_pw_hash(name, pw)
        return User(name = name,
                    pw_hash = pw_hash,
                    email = email)
        
    @classmethod
    def check_login(cls, name, pw):
        user = cls.by_name(name)
        if user and cls.valid_pw(name, pw, user.pw_hash):
            return user

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        params["user"] = self.user
        t = JINJA_ENV.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
    def make_secure_val(self, val):
        return "%s|%s" % (val, hmac.new(secret, val).hexdigest())
        
    def check_secure_val(self, secure_val):
        val = secure_val.split('|')[0]
        if secure_val == self.make_secure_val(val):
            return val
        
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and self.check_secure_val(cookie_val)
        
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie("user_id")
        self.user = uid and User.by_id(int(uid)) #mystery: no idea why this is assigned a User obj shouldn't it be a boolean?
        if self.request.url.endswith(".json"):
            self.format = "json"
        else:
            self.format = "html"
