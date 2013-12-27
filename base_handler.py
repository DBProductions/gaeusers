# -*- coding: utf-8 -*-
import webapp2, jinja2, os
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from app_languages import *

class BaseHandler(webapp2.RequestHandler):
    def getTemp(self, temp_file, temp_vars):
        """
        Get a rendered template.
        
        Parameters
        ----------
        temp_file: the html file

        temp_vars: dict with values for the template

        Returns
        -------
        A rendered template.
        """
        template = jinja_environment.get_template('templates/' + temp_file)
        return template.render(temp_vars)
    def getLocale(self):
        """
        Get the current language from cookie or as url parameter.
        Set default value when not present, set for application and set cookie.

        Returns
        -------
        The current language.
        """
        userlocale = self.request.cookies.get('gaeuserlocale', '')
        urllocale = self.request.get("locale")
        if not urllocale:
            if not userlocale:
                locale = 'en'
            else:
                locale = userlocale
        else:
            locale = urllocale
            self.response.headers.add_header('Set-Cookie', 'gaeuserlocale='+str(locale)+'; expires=31-Dec-202023:59:59 GMT')
        return locale
    def getMsgsForKey(self, key):
        """
        Get messages for a specific key.

        Parameters
        ----------
        key: section key

        Returns
        -------
        dict - with specific messages
        """
        locale = self.getLocale()
        uitext = responsemsgs[locale]
        return uitext[key]
    def getTplText(self, key):
        """
        get placeholder for template
        """
        locale = self.getLocale()
        uitext = responsemsgs[locale]
        text = ''
        if key == 'uiindex':
            text = {'title': uitext['uiindex']['title'],
                    'headline': uitext['uiindex']['headline'],   
                    'login': uitext['uiindex']['login'],
                    'loginbtn': uitext['uiindex']['loginbtn'],
                    'email': uitext['uiindex']['email'],
                    'password': uitext['uiindex']['password'], 
                    'repassword': uitext['uiindex']['repassword'],                     
                    'losepw': uitext['uiindex']['losepw'], 
                    'register': uitext['uiindex']['register'],
                    'registerbtn': uitext['uiindex']['registerbtn']}
        elif key == 'uiconform':
            text = {'title': uitext['uiconform']['title'],
                    'backbtn': uitext['uiconform']['backbtn']}
        elif key == 'uilosepw':
            text = {'title': uitext['uilosepw']['title'],
                    'email': uitext['uilosepw']['email'],
                    'send': uitext['uilosepw']['send'],
                    'back': uitext['uilosepw']['back']}
        elif key == 'uiprofile':
            text = {'title': uitext['uiprofile']['title'],
                    'changepw': uitext['uiprofile']['changepw'],
                    'delaccount': uitext['uiprofile']['delaccount'],
                    'logout': uitext['uiprofile']['logout'],
                    'headline': uitext['uiprofile']['headline']}
        elif key == 'uichangepw':
            text = {'title': uitext['uichangepw']['title'],
                    'profile': uitext['uichangepw']['profile'],
                    'changepw': uitext['uichangepw']['changepw'],
                    'delaccount': uitext['uichangepw']['delaccount'],
                    'logout': uitext['uichangepw']['logout'],
                    'oldpassword': uitext['uichangepw']['oldpassword'],
                    'newpassword': uitext['uichangepw']['newpassword'],
                    'renewpassword': uitext['uichangepw']['renewpassword']}
        elif key == 'uisetpw':
            text = {'title': uitext['uisetpw']['title'],
                    'newpassword': uitext['uisetpw']['newpassword'],
                    'renewpassword': uitext['uisetpw']['renewpassword'],
                    'back': uitext['uisetpw']['back']}
        elif key == 'uidelaccount':
            text = {'title': uitext['uidelaccount']['title'],
                    'profile': uitext['uidelaccount']['profile'],
                    'changepw': uitext['uidelaccount']['changepw'],
                    'delaccount': uitext['uidelaccount']['delaccount'],
                    'delete': uitext['uidelaccount']['delete'],
                    'logout': uitext['uidelaccount']['logout']}
        text['locale'] = locale
        return text