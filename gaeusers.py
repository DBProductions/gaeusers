# -*- coding: utf-8 -*-
import os
import random
import re
import hashlib
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
    language = db.StringProperty(default='en')

class ActiveLinks(db.Model):
    user = db.StringProperty()
    link = db.StringProperty()

class PasswordLinks(db.Model):
    user = db.StringProperty()
    link = db.StringProperty()

class GaeUsers():
    """
    GaeUsers
    """
    def __init__(self, options):
        """
        Init gaeusers with options.

        Parameters
        ----------
        options - dict
            appid
            mailstring
            crypt
            crypt_rounds
            password_salt
        """
        self.backlink = 'https://' + options['appid'] + '.appspot.com/conform?link='
        self.passlink = 'https://' + options['appid'] + '.appspot.com/setpassword?link='
        self.password_salt = options['password_salt']
        self.crypt_rounds = options['crypt_rounds']
        self.mailstring = options['mailstring']
        self.crypt = options['crypt']

    def check_userkey(self, key):
        """
        Check if user key exists in memcache.

        Parameters
        ----------
        key: key in memcache
        """
        return memcache.get(key)

    def set_userkey(self, email, db_key, set_cache):
        """
        Set user key.
        """
        userkey = email + '_' + str(db_key)
        userkey = self.crypt_string(userkey)                        
        if set_cache == True:
            memcache.add(userkey, str(db_key))
        return userkey 

    def get_useremail(self, key):
        """
        Get user email.

        Parameters
        ----------
        key: key in memcache

        Returns
        -------
        Email from the user as string.
        """
        key = memcache.get(key)
        u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(key))
        uresult = u_query.get()
        return str(uresult.email)

    def get_passworduser(self, link):
        """
        Get user who want to change password.

        Parameters
        ----------
        link: link in data store

        Returns
        -------
        Returns the user key as string or None.
        """
        u_query = db.GqlQuery("SELECT * FROM PasswordLinks WHERE link = :1", str(link))
        uresult = u_query.get()
        if uresult:
            return str(uresult.user)
        else:
            return None

    def get_user(self, key):
        """
        Get a user from data store.

        Parameters
        ----------
        key: key in the data store

        Returns
        -------
        Users data store object.
        """
        u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(key))
        uresult = u_query.get()
        return uresult

    def crypt_string(self, string):
        """
        Crypt string

        Parameters
        ----------
        string: string to be crypt

        Returns
        -------
        A crypt string.
        """
        if self.crypt == 'md5':
            for i in range(self.crypt_rounds):
                crypt_string = hashlib.md5(self.password_salt + string).hexdigest()
            return crypt_string
        elif self.crypt == 'sha1':
            for i in range(self.crypt_rounds):
                crypt_string = hashlib.sha1(self.password_salt + string).hexdigest()
            return crypt_string

    def register(self, email, password, repassword, lang, subject):
        """
        Register a user.

        Parameters
        ----------
        email: email to register

        password: password to register

        repassword: repeat of password to register

        lang: current language

        subject: email subject

        Returns
        -------
        dict - Response
            register
            error
            key
        """
        if email != '':
            check = False
            if len(email) > 5:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                    if password == repassword:
                        check = True          
                    else:
                        return dict(register=False, error="not equal")
            if check == False:
                return dict(register=False, error="not valid")
            else:
                query = db.GqlQuery("SELECT * FROM Users WHERE email= :1", email)
                result = query.get()
                if result:
                    return dict(register=False, error="present")
                else:
                    password = self.crypt_string(password)            
                    u = Users(email = email, password = password, active = False, language = lang)
                    u.put()
                    link_key = str( random.randrange(0, 10001, 2) + 1000 )
                    link_key = self.crypt_string(link_key)
                    link = self.backlink + link_key
                    l = ActiveLinks(user=str(u.key()),link=link_key)
                    l.put()
                    userkey = self.set_userkey(email, str(u.key()), False)
                    tpl = 'templates/emails/activate_' + lang + '.html'
                    messagebody = template.render(tpl, {'link': link}) 
                    mail.send_mail(sender=self.mailstring, to="<"+email+">", subject=subject, body=messagebody)
                    return dict(register=True, key=userkey)
        else:
            return dict(register=False, error="empty")

    def lose_password(self, email, lang, subject):
        """
        Lose password request.

        Parameters
        ----------
        email: email from the requesting user

        lang: selected languageto select the right template

        subject: mail subject

        Returns
        -------
        dict - Response
            response
        """
        u_query = db.GqlQuery("SELECT * FROM Users WHERE email = :1", email)
        uresult = u_query.get()
        if uresult:
            p_query = db.GqlQuery("SELECT * FROM PasswordLinks WHERE user = :1", str(uresult.key()))
            presult = p_query.get()
            if presult:
                link_key = presult.link
            else:
                link_key = str( random.randrange(0, 10001, 2) + 1000 )
                link_key = self.crypt_string(link_key)
                l = PasswordLinks(user=str(uresult.key()), link=link_key)
                l.put()
            link = self.passlink + link_key            
            tpl = 'templates/emails/losepassword_' + lang + '.html'
            messagebody = template.render(tpl, {'link':link})
            mail.send_mail(sender=self.mailstring, to="<"+uresult.email+">", subject=subject, body=messagebody)
            return dict(response=True)
        else:
            return dict(response="empty")

    def set_password(self, link, password, repassword):
        """
        Set a password.

        Parameters
        ----------
        password: the new password

        repassword: the new password as repeat

        Returns
        -------
        dict - Response
            response
        """
        query = db.GqlQuery("SELECT * FROM PasswordLinks WHERE link = :1", link)
        result = query.get()
        if result:            
            if password != repassword:
                return dict(response='not equal')
            else:
                u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(result.user))
                uresult = u_query.get()
                password = self.crypt_string(password)
                uresult.password = password
                uresult.put()
                db.delete(result)
                return dict(response='set')
        else:
            return dict(response='not present')

    def change_password(self, userkey, passwordold, newpassword, renewpassword):
        """
        Change a password.

        Parameters
        ----------
        passwordold: the current password

        newpassword: the new password

        renewpassword: the new password as repeat

        Returns
        -------
        dict - Response
            response
        """
        key = memcache.get(userkey)
        u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(key))
        uresult = u_query.get()
        passwordold = self.crypt_string(passwordold)        
        if uresult.password == passwordold:
            if newpassword == renewpassword:
                newpassword = self.crypt_string(newpassword)                
                uresult.password = newpassword
                uresult.put()
                return dict(response="change")
            else:
                return dict(response="not equal")
        else:
            return dict(response="wrong")

    def conform(self, link):
        """
        Conform registration and activate the user.

        Parameters
        ----------
        link: link send via email

        Returns
        -------
        dict - Response
            response
        """
        query = db.GqlQuery("SELECT * FROM ActiveLinks WHERE link = :1", link)
        result = query.fetch(1)
        if result:
            u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(result[0].user))
            uresult = u_query.get()
            uresult.active = True
            db.put(uresult)
            db.delete(result)
            return dict(response=True)
        else:
            return dict(response=False)

    def login(self, email, password):
        """
        Authorize a user with credentials.

        Parameters
        ----------
        email: Email from user

        password: Password from user

        Returns
        -------
        dict - Response 
            login
            key
        """
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
                        userkey = self.set_userkey(email, str(result.key()), True)
                        return dict(login=True, key=userkey)
                    else:
                        return dict(login=False)
                else:
                    return dict(login="not active")
            else:
                return dict(login="unknown")
        else:
            return dict(login="empty")

    def logout(self, key):
        """
        Delete key from memcache.

        Parameters
        ----------
        key: key in memcache to delete
        """
        memcache.delete(key)

    def deleteaccount(self, key):
        """
        Delete a user account.

        Parameters
        ----------
        key: key in memcache for the user to delete
        """
        userkey = memcache.get(key)        
        u_query = db.GqlQuery("SELECT * FROM Users WHERE __key__ = :1", db.Key(userkey))
        user = u_query.get()
        db.delete(user)
        memcache.delete(key)