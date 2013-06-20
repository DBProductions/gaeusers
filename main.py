import os, datetime, hashlib, webapp2, json, jinja2
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from gaeusers import *

# options for gaeusers
options = {'appid': 'gae-users', 'mailstring': 'your_name <your_email>', 'crypt':'md5'}
gaeusers = GaeUsers(options)

responsemsgs = {
    'login': {'false':'Not right combination.',
              'not active':'Account is not activated.',
              'unknown':'Not right combination.',
              'empty':'Email is empty.'},
    'register': {'not equal':'Passwords are not equal.',
                 'not valid':'Email is not valid.',
                 'present':'Email is registered.',
                 'empty':'Email is empty.',
                 'end':'Now activate your acount with visiting the link we send to you.'},
    'conform': {'true':'You have activate your account successful.',
                'false':'There is no account which can get activated.'},
    'losepassword': {'empty':'Not registered.',
                     'true':'Email send successful.'},
    'changepassword': {'change':'Your password has been changed.',
                       'not equal': 'New password not equal.',
                       'wrong':'Your password hasn\'t been changed.'}
}

class BaseHandler(webapp2.RequestHandler):
    """BaseHandler to extend"""
    def getTemp(self, temp_file, temp_vars):
        template = jinja_environment.get_template('templates/' + temp_file)
        return template.render(temp_vars)

class MainHandler(BaseHandler):
    """MainHandler for index or profile"""
    def get(self):
        userkey = self.request.cookies.get('gaeuserkey', '')
        if None == gaeusers.check_userkey(userkey):
            self.response.out.write(self.getTemp("index.html", {}))
        else:
            email = gaeusers.get_useremail(userkey)
            self.response.out.write(self.getTemp("profile.html", {'email':email}))

class LoginHandler(BaseHandler):
    """LoginHandler for login"""
    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")        
        loginresponse = gaeusers.login(email, password)
        responseobj = json.loads(loginresponse)             
        if 'key' in responseobj['login']:
            self.response.headers.add_header('Set-Cookie', 'gaeuserkey='+str(responseobj['login']['key'])+'; expires=31-Dec-202023:59:59 GMT')
            self.redirect('/')
        else:
            responsemsg = responsemsgs['login'][responseobj['login']['check']]
            self.response.out.write(self.getTemp("index.html", {'msg':responsemsg}))            

class LogoutHandler(webapp2.RequestHandler):
    """LogoutHandler for logout"""
    def get(self):
        userkey = username = self.request.cookies.get('gaeuserkey', '')
        gaeusers.logout(userkey)
        self.redirect('/')
        
class RegisterHandler(BaseHandler):
    """RegisterHandler for register"""
    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")
        repassword = self.request.get("repassword")
        registerresponse = gaeusers.register(email, password, repassword)
        responseobj = json.loads(registerresponse)
        if 'key' in responseobj['register']:
            self.response.out.write(self.getTemp("index.html", {'rmsg':responsemsgs['register']['end']}))
        else:            
            responsemsg = responsemsgs['register'][responseobj['register']['check']]
            self.response.out.write(self.getTemp("index.html", {'rmsg':responsemsg}))

class ConformHandler(BaseHandler):
    """ConformHandler for conform"""
    def get(self):
        confirm_link = self.request.get("link")
        response = gaeusers.conform(confirm_link)
        responseobj = json.loads(response)
        responsemsg = responsemsgs['conform'][responseobj['response']['conform']]
        self.response.out.write(self.getTemp("conform.html", {"msg":responsemsg}))

class LosepasswordHandler(BaseHandler):
    """LosepasswordHandler"""
    def get(self):
        self.response.out.write(self.getTemp("losepass.html", {}))
    def post(self):
        email = self.request.get("email")
        response = gaeusers.lose_password(email)
        responseobj = json.loads(response)
        responsemsg = responsemsgs['losepassword'][responseobj['response']['send']]
        if responseobj['response']['send'] == 'true':
            self.response.out.write(self.getTemp("losepass.html", {"msg":responsemsg}))
        else:
            self.response.out.write(self.getTemp("losepass.html", {"msg":responsemsg}))

class ChangepasswordHandler(BaseHandler):
    """ChangepasswordHandler"""
    def get(self):
        userkey = username = self.request.cookies.get('gaeuserkey', '')
        self.response.out.write(self.getTemp("changepass.html", {'key':userkey}))
    def post(self):
        key = self.request.get("key")
        passwordold = self.request.get("passwordold")
        newpassword = self.request.get("newpassword")
        renewpassword = self.request.get("renewpassword")
        response = gaeusers.change_password(key, passwordold, newpassword, renewpassword)
        responseobj = json.loads(response)
        responsemsg = responsemsgs['changepassword'][responseobj['response']['check']]
        self.response.out.write(self.getTemp("changepass.html", {"key":key,"msg":responsemsg}))
        
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/register', RegisterHandler),                                      
                               ('/conform', ConformHandler),
                               ('/losepassword', LosepasswordHandler),
                               ('/changepassword', ChangepasswordHandler)], debug=True)
