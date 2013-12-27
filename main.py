# -*- coding: utf-8 -*-
from gaeusers import *
from base_handler import *

# options for gaeusers
options = {'appid': 'gaeusers', 
           'mailstring': 'your_name <your_email>', 
           'crypt':'md5',
           'crypt_rounds': 10,
           'password_salt':'xyz987'}

gaeusers = GaeUsers(options)

class MainHandler(BaseHandler):
    def get(self):
        """
        Show index or profile view
        """
        userkey = self.request.cookies.get('gaeuserkey', '')
        if None == gaeusers.check_userkey(userkey):
            tpl_data = self.getTplText('uiindex')
            self.response.out.write(self.getTemp("index.html", tpl_data))
        else:
            tpl_data = self.getTplText('uiprofile')
            tpl_data['email'] = gaeusers.get_useremail(userkey)
            self.response.out.write(self.getTemp("profile.html", tpl_data))

class LoginHandler(BaseHandler):
    def post(self):
        """
        Login a user on request.
        """
        email = self.request.get("email")
        password = self.request.get("password")        
        loginresponse = gaeusers.login(email, password)         
        if 'key' in loginresponse:
            self.response.headers.add_header('Set-Cookie', 'gaeuserkey='+str(loginresponse['key'])+'; expires=31-Dec-202023:59:59 GMT')
            self.redirect('/')
        else:
            tpl_data = self.getTplText('uiindex')
            error_msg =self.getMsgsForKey('login')
            tpl_data['msg'] = error_msg[str(loginresponse['login'])]
            tpl_data['error'] = True
            self.response.out.write(self.getTemp("index.html", tpl_data))            

class LogoutHandler(BaseHandler):
    def get(self):
        """
        Get cookie, call logout method, delete cookie and redirect to startpage.
        """
        userkey = self.request.cookies.get('gaeuserkey', '')
        gaeusers.logout(userkey)
        self.response.headers.add_header('Set-Cookie', 'gaeuserkey='+str(userkey)+'; expires=0')
        self.redirect('/')
        
class RegisterHandler(BaseHandler):
    def post(self):
        """
        Register a user on request.
        """
        email = self.request.get("email")
        password = self.request.get("password")
        repassword = self.request.get("repassword")
        email_subject = self.getMsgsForKey('mailsubjects')
        reg_response = gaeusers.register(email, password, repassword, self.getLocale(), email_subject['activate'])
        tpl_data = self.getTplText('uiindex')
        error_msg = self.getMsgsForKey('register')
        if 'key' in reg_response:
            tpl_data['rmsg'] = error_msg['end']
            self.response.out.write(self.getTemp("index.html", tpl_data))
        else:
            tpl_data['rmsg'] = error_msg[reg_response['error']]
            tpl_data['error'] = True
            self.response.out.write(self.getTemp("index.html", tpl_data))

class ConformHandler(BaseHandler):
    def get(self):
        """
        Show template on request.
        """
        confirm_link = self.request.get("link")
        response = gaeusers.conform(confirm_link)
        tpl_data = self.getTplText('uiconform')
        error_msg = self.getMsgsForKey('conform')
        tpl_data['msg'] = error_msg[str(response['response'])]
        self.response.out.write(self.getTemp("conform.html", tpl_data))

class LosepasswordHandler(BaseHandler):
    def get(self):
        """
        Show template with form on request.
        """
        tpl_data = self.getTplText('uilosepw')
        self.response.out.write(self.getTemp("losepass.html", tpl_data))
    def post(self):
        """
        Show template with message on request.
        """
        email = self.request.get("email")
        email_subject = self.getMsgsForKey('mailsubjects')
        response = gaeusers.lose_password(email, self.getLocale(), email_subject['pwchange'])
        tpl_data = self.getTplText('uilosepw')
        error_msg = self.getMsgsForKey('losepassword')
        tpl_data['msg'] = error_msg[str(response['response'])]
        if response['response'] == True:
            self.response.out.write(self.getTemp("losepass.html", tpl_data))
        else:
            tpl_data['error'] = True
            self.response.out.write(self.getTemp("losepass.html", tpl_data))

class DeleteAccountHandler(BaseHandler):
    def get(self):
        """
        Show template with form on request.
        """
        userkey = self.request.cookies.get('gaeuserkey', '')
        email = gaeusers.get_useremail(userkey)
        tpl_data = self.getTplText('uidelaccount')
        tpl_data['email'] = email
        tpl_data['key'] = userkey
        self.response.out.write(self.getTemp("deleteaccount.html", tpl_data))
    def post(self):
        """
        Delete account on request.
        """
        delete = self.request.get("delete")
        if delete == 'on':
            userkey = self.request.cookies.get('gaeuserkey', '')
            gaeusers.deleteaccount(userkey)
            gaeusers.logout(userkey)
            self.response.headers.add_header('Set-Cookie', 'gaeuserkey='+str(userkey)+'; expires=0')
            self.redirect('/')
        else:
            self.redirect('/delaccount')

class SetPasswordHandler(BaseHandler):
    def get(self):
        """
        Show template with form on GET Request
        """
        userkey = self.request.cookies.get('gaeuserkey', '')
        link = self.request.get("link")
        tpl_data = self.getTplText('uisetpw')
        error_msg = self.getMsgsForKey('setpassword')
        tpl_data['link'] = link
        if link == '':
            tpl_data['error'] = 'true'
            tpl_data['msg'] = error_msg['not present']
        self.response.out.write(self.getTemp("setpass.html", tpl_data))
    def post(self):
        """
        Set a new password.
        """
        link = self.request.get("link")
        newpassword = self.request.get("newpassword")
        renewpassword = self.request.get("renewpassword")
        tpl_data = self.getTplText('uisetpw')
        error_msg = self.getMsgsForKey('setpassword')
        user = gaeusers.get_passworduser(link)
        if user is not None:
            userObj = gaeusers.get_user(user)
            response = gaeusers.set_password(link, newpassword, renewpassword)
            tpl_data['msg'] = error_msg[response['response']]
            if response['response'] == 'set':
                tpl_data['btn'] = True
        else:
            tpl_data['error'] = 'true'
            tpl_data['msg'] = error_msg['not present']
        tpl_data['link'] = link
        self.response.out.write(self.getTemp("setpass.html", tpl_data))


class ChangepasswordHandler(BaseHandler):
    def get(self):
        """
        Show template with form.
        """
        userkey = self.request.cookies.get('gaeuserkey', '')
        if gaeusers.check_userkey(userkey) is not None:
            email = gaeusers.get_useremail(userkey)
            tpl_data = self.getTplText('uichangepw')
            tpl_data['email'] = email
            tpl_data['key'] = userkey
            self.response.out.write(self.getTemp("changepass.html", tpl_data))
        else:
            self.redirect('/')        
    def post(self):
        """
        Change the password.
        """
        key = self.request.get("key")
        email = gaeusers.get_useremail(key)
        passwordold = self.request.get("passwordold")
        newpassword = self.request.get("newpassword")
        renewpassword = self.request.get("renewpassword")        
        response = gaeusers.change_password(key, passwordold, newpassword, renewpassword)
        tpl_data = self.getTplText('uichangepw')
        error_msg = self.getMsgsForKey('changepassword')
        tpl_data['email'] = email
        tpl_data['msg'] = error_msg[response['response']]
        tpl_data['key'] = key
        if 'change' != response['response']:
            tpl_data['error'] = True
        self.response.out.write(self.getTemp("changepass.html", tpl_data))
        
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/register', RegisterHandler),                                      
                               ('/conform', ConformHandler),
                               ('/losepassword', LosepasswordHandler),
                               ('/setpassword', SetPasswordHandler),
                               ('/changepassword', ChangepasswordHandler),
                               ('/delaccount', DeleteAccountHandler)], debug=True)
