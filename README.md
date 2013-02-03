# App Engine user management with gaeusers

The gaeusers module offers a basic user management for your apps which running on App Engine and written in Python.

    from gaeusers import *
	options = {'appid': '<app-id>', 'mailstring': 'your_name <your_email>', 'crypt':'md5'}
	gaeusers = GaeUsers(options)
	
After creating an instance of gaeusers, it offers the following methods.

    register_response = gaeusers.register(email)
	login_response = gaeusers.login(email, pw)
	confirm_response = gaeusers.conform(confirm_link)
	losepassword_response = gaeusers.lose_password(email)
	changepassword_response = gaeusers.change_password(key, pw_old, pw_new, pw_renew)
	
How to use it, is shown in `main.py` templates using the bootstrap framework.