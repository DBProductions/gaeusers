import os, datetime, hashlib, webapp2, json
from google.appengine.ext.webapp import template

from gaeusers import *

# options for gaeusers
options = {'appid': '<app-id>', 'mailstring': 'your_name <your_email>', 'crypt':'md5'}
gaeusers = GaeUsers(options)

class BaseHandler(webapp2.RequestHandler):
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
            self.response.headers.add_header('Set-Cookie', 'gaeuserkey='+str(loginresponseobj['login']['key'])+'; expires=31-Dec-202023:59:59 GMT')
            self.redirect('/')
        else:
            self.response.out.write( self.getTemp("index.html", {'msg':loginresponseobj['login']['check']}) )            

class LogoutHandler(webapp2.RequestHandler):
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
        if 'key' in registerresponseobj['register']:
            self.response.out.write('now activate your acount with visiting the link we send you')
        else:
            self.response.out.write(self.getTemp("index.html", {'rmsg':registerresponseobj['register']['check']}))

class ConformHandler(webapp2.RequestHandler):
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
        self.response.out.write(self.getTemp("losepass.html", {"msg":"Email send successful: " + responseobj['response']['send']}))

class ChangepasswordHandler(BaseHandler):
    def get(self):
        userkey = username = self.request.cookies.get('gaeuserkey', '')
        self.response.out.write( self.getTemp("changepass.html", {'key':userkey}) )
    def post(self):
        key = self.request.get("key")
        passwordold = self.request.get("passwordold")
        newpassword = self.request.get("newpassword")
        renewpassword = self.request.get("renewpassword")
        response = gaeusers.change_password(key, passwordold, newpassword, renewpassword)
        responseobj = json.loads(response)
        if 'change' == responseobj['response']['check']:
            msg = 'Your password has been changed.'
        elif 'wrong' == responseobj['response']['check']:
            msg = 'Your password hasn\'t been changed.'
        self.response.out.write( self.getTemp("changepass.html", {"key":key,"msg":msg}) )
        
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/register', RegisterHandler),                                      
                               ('/conform', ConformHandler),
                               ('/losepassword', LosepasswordHandler),
                               ('/changepassword', ChangepasswordHandler)], debug=True)
