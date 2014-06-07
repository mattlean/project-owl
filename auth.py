from google.appengine.ext import db
from handler import Handler
from string import letters
import hashlib
import hmac
import random
import re

secret = "itsasecrettoeveryone"

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

class AuthHandler(Handler):
    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return username and USER_RE.match(username)
    
    def valid_password(self, password):
        PASS_RE = re.compile(r"^.{3,20}$")
        return password and PASS_RE.match(password)
    
    def valid_email(self, email):
        EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        return not email or EMAIL_RE.match(email)
    
    def make_secure_val(self, val):
        return "%s|%s" % (val, hmac.new(secret, val).hexdigest())
    
    def set_secure_cookie(self, name, val):
        cookie_val = self.make_secure_val(val)
        self.response.headers.add_header("Set-Cookie", "%s=%s; Path=/" % (name, cookie_val))

    def login(self, user):
        self.set_secure_cookie("user_id", str(user.key().id()))

    def logout(self):
        self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")

class Register(AuthHandler):
    def get(self):
        self.render("register.html")
        
    def post(self):
        have_error = False
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify = self.request.get("verify")
        self.email = self.request.get("email")       
        params = dict(username = self.username, email = self.email)
                
        if not self.valid_username(self.username):
            params["error_username"] = "Invalid username!"
            have_error = True
        
        if not self.valid_password(self.password):
            params["error_password"] = "Invalid password!"
            have_error = True
        elif self.password != self.verify:
            params["error_verify"] = "Your passwords didn't match!"
            have_error = True
            
        if not self.valid_email(self.email):
            params["error_email"] = "Invalid email!"
            have_error = True
            
        if have_error:
            self.render("register.html", **params)
        else:
            u = User.by_name(self.username)
            if u:
                msg = "That username already exists!"
                self.render("register.html", error_username = msg)
            else:
                u = User.create_user(self.username, self.password, self.email)
                u.put()
                self.login(u)
                self.redirect('/')

class Login(AuthHandler):
    def get(self):
        self.render("login.html")
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        
        user = User.check_login(username, password)
        if user:
            self.login(user)
            self.redirect('/')
        else:
            msg = "Invalid login!"
            self.render("login.html", username = username, error = msg)

class Logout(AuthHandler):
    def get(self):
        self.logout()
        self.redirect('/')
