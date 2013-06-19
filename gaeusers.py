import os, random, re, hashlib
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class Users(db.Model):
    email = db.StringProperty(required=True)
    password = db.StringProperty()
    active = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    logins = db.IntegerProperty()
    lastlogin = db.DateTimeProperty(auto_now=True)

class ActiveLinks(db.Model):
    user = db.StringProperty()
    link = db.StringProperty()

class GaeUsers():    
    def __init__(self, options):
        """init gaeusers with options"""
        self.backlink = 'http://' + options['appid'] + '.appspot.com/conform?link='
        self.mailstring = options['mailstring']
        self.CRYPT = options['crypt']            
    def check_userkey(self, key):
        """check if user key exists"""
        return memcache.get(key)          
    def get_useremail(self, key):
        """get user email"""
        key = memcache.get(key)
        u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(key))
        uresult = u_query.get()
        return str(uresult.email)  
    def crypt_string(self, string):
        """crypt string"""
        if self.CRYPT == 'md5':
            return hashlib.md5(string).hexdigest()
        elif self.CRYPT == 'sha1':
            return hashlib.sha1(string).hexdigest()    
    def register(self, email, password, repassword):
        """register a user"""
        if email != '':
            check = False
            if len(email) > 5:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                    if password == repassword:
                        check = True          
                    else:
                        return '{"register":{"check":"not equal"}}'
            if check == False:
                return '{"register":{"check":"not valid"}}'
            else:
                query = db.GqlQuery("SELECT * FROM Users WHERE email= :1", email)
                result = query.get()
                if result:
                    return '{"register":{"check":"present"}}'
                else:
                    password = self.crypt_string(password)            
                    u = Users(email = email, password = password, active = False)
                    u.put()
                    link_key = str( random.randrange(0, 101, 2) )
                    link = self.backlink + link_key
                    l = ActiveLinks(user=str(u.key()),link=link_key)
                    l.put()
                    userkey = email + '_' + str(u.key())
                    userkey = self.crypt_string(userkey)                        
                    memcache.add(userkey, str(u.key()))
                    messagebody = template.render('templates/email.html', {'link': link}) 
                    mail.send_mail(sender=self.mailstring, to="<"+email+">", subject="User registration", body=messagebody)
                    return '{"register":{"check":"true", "key": "' + userkey + '"}}'
        else:
            return '{"register":{"check":"empty"}}'    
    def lose_password(self, email):
        """lose password"""
        u_query = db.GqlQuery("SELECT * FROM Users WHERE email = :1", email)
        uresult = u_query.get()
        if uresult:
            messagebody = template.render('templates/email.html', {'password':uresult.password, 'link': ''})
            mail.send_mail(sender=self.mailstring, to="<"+uresult.email+">", subject="User password", body=messagebody)
            return '{"response":{"send":"true"}}'
        else:
            return '{"response":{"send":"empty"}}'    
    def change_password(self, userkey, passwordold, newpassword, renewpassword):
        """change a password"""
        key = memcache.get(userkey)
        u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(key))
        uresult = u_query.get()
        passwordold = self.crypt_string(passwordold)        
        if uresult.password == passwordold:
            if newpassword == renewpassword:
                newpassword = self.crypt_string(newpassword)                
                uresult.password = newpassword
                uresult.put()
                return '{"response":{"check":"change"}}'
            else:
                return '{"response":{"check":"not equal"}}'
        else:
            return '{"response":{"check":"wrong"}}'    
    def conform(self, link):
        """conform registration"""
        query = db.GqlQuery("SELECT * FROM ActiveLinks WHERE link = :1", link)
        result = query.fetch(1)
        if result:
            u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(result[0].user))
            uresult = u_query.get()
            uresult.active = True
            db.put(uresult)
            db.delete(result)
            return '{"conform": "true"}'
        else:
            return '{"conform": "false"}'    
    def login(self, email, password):
        """do login"""
        if email != '' and password != '':
            password = self.crypt_string(password)    
            query = db.GqlQuery("SELECT * FROM Users WHERE email = :1 AND password = :2", email, password)
            result = query.get()
            if result:
                if result.active == True:                    
                    if email == result.email:                    
                        if result.logins != None:
                            result.logins = result.logins + 1
                        else:
                            result.logins = 1
                        result.put()
                        userkey = email + '_' + str(result.key())
                        userkey = self.crypt_string(userkey)                        
                        memcache.add(userkey, str(result.key()))
                        return '{"login":{"check": "true","key": "' + userkey + '"}}'
                    else:
                        return '{"login":{"check": "false"}}'
                else:
                    return '{"login":{"check": "not active"}}'
            else:
                return '{"login":{"check": "unknown"}}'
        else:
            return '{"login":{"check":"empty"}}'
    def logout(self, key):
        """do logout"""
        memcache.delete(key)