#  gaeusers

A simple user management for App Engine applications.

Users can register, activate their accounts via email and only activated user are able to login.  
After a successful login the user ends on the profil page where they can change their password or delete their account.  
When the password is lost, the user is able to set a new one.

There is a `BaseHandler` defined to handle templates in different languages.  
The languages are defined in `app_languages.py`.  

A set of basic templates are defined, email templates are in a subfolder.

### Documentation:  
[GitHub Page](http://dbproductions.github.com/gaeusers/)

### Live example:  
[Appspot](http://gae-users.appspot.com/)

## Feedback
Star this repo if you found it useful. Use the github issue tracker to give feedback on this repo.
