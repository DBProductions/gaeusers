import os, datetime, hashlib, logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json

from gaeusers import *

# options for gaeusers
options = {'backlink': 'http://<app-id>.appspot.com/conform?link=', 'mailstring': 'your_name <your_email>', 'crypt':'md5'}
gaeusers = GaeUsers(options)

class BaseHandler(webapp.RequestHandler):
    def getTemp(self, temp_file, temp_vars):
        path = os.path.join(os.path.dirname(__file__), 'templates/' + temp_file)
        return template.render(path, temp_vars)

class MainHandler(BaseHandler):
    def get(self):        
        userkey = username = self.request.cookies.get('gaeuserkey', '')
        if None == gaeusers.check_userkey(userkey):
            self.response.out.write( self.getTemp("index.html", {}) )
        else:
            self.response.out.write( self.getTemp("profile.html", {}) )

class LoginHandler(BaseHandler):
    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")        
        loginresponse = gaeusers.login(email, password)
        loginresponseobj = json.loads( loginresponse )             
        if 'key' in loginresponseobj['login']:
            self.response.headers.add_header('Set-Cookie', 'gaeuserkey='+loginresponseobj['login']['key']+'; expires=31-Dec-202023:59:59 GMT')
            self.redirect('/')
        else:
            self.response.out.write( self.getTemp("index.html", {'msg':loginresponseobj['login']['check']}) )            

class LogoutHandler(webapp.RequestHandler):
    def get(self):
        userkey = username = self.request.cookies.get('gaeuserkey', '')
        gaeusers.logout(userkey)
        self.redirect('/')
        
class RegisterHandler(BaseHandler):
    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")
        repassword = self.request.get("repassword")
        registerresponse = gaeusers.register(email, password, repassword)
        registerresponseobj = json.loads(registerresponse)
        logging.info(registerresponseobj)
        if 'key' in registerresponseobj['register']:
            self.response.out.write('now activate your acount with visiting the link we send you')
        else:
            self.response.out.write(self.getTemp("index.html", {'rmsg':registerresponseobj['register']['check']}))

class ConformHandler(webapp.RequestHandler):
    def get(self):
        confirm_link = self.request.get("link")
        self.response.out.write(gaeusers.conform(confirm_link))

class LosepasswordHandler(BaseHandler):
    def get(self):
        self.response.out.write(self.getTemp("losepass.html", {}))
    def post(self):
        email = self.request.get("email")
        response = gaeusers.lose_password(email)
        responseobj = json.loads(response)
        #self.response.out.write(gaeusers.lose_password(email))
        self.response.out.write(self.getTemp("losepass.html", {"msg":responseobj['response']['send']}))

class ChangepasswordHandler(BaseHandler):
    def get(self):
        userkey = username = self.request.cookies.get('gaeuserkey', '')
        self.response.out.write( self.getTemp("changepass.html", {'key':userkey}) )
    def post(self):
        key = self.request.get("key")
        passwordold = self.request.get("passwordold")
        newpassword = self.request.get("newpassword")
        renewpassword = self.request.get("renewpassword")             
        self.response.out.write(gaeusers.change_password(key, passwordold, newpassword, renewpassword))
        
application = webapp.WSGIApplication([('/', MainHandler),
                                      ('/login', LoginHandler),
                                      ('/logout', LogoutHandler),
                                      ('/register', RegisterHandler),                                      
                                      ('/conform', ConformHandler),
                                      ('/losepassword', LosepasswordHandler),
                                      ('/changepassword', ChangepasswordHandler)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()