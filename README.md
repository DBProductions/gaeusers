# App Engine user management with gaeusers

The gaeusers module offers a basic user management for your apps which running on App Engine and written in Python.

    from gaeusers import *
	options = {'backlink': 'http://<app-id>.appspot.com/conform?link=', 'mailstring': 'your_name <your_mail>', 'crypt':'md5'}
	gaeusers = GaeUsers(options)
	
After creating an instance of gaeusers, it offers the following methods.

    register_response = gaeusers.register(email)
    
	login_response = gaeusers.login(email, password)
	
	confirm_response = gaeusers.conform(confirm_link)
	
	losepassword_response = gaeusers.lose_password(email)
	
	changepassword_response = gaeusers.change_password(key, password_old, password_new, password_renew)
	
A basic structure how to use it, is shon in `main.py`