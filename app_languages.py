# -*- coding: utf-8 -*-
# username 用户名
responsemsgs = {
    'zh': {
        'uiindex' : {
            'title': 'GAE Users',
            'headline': unicode('欢迎', 'utf8'),
            'login': unicode('注册', 'utf8'),
            'email': unicode('电邮', 'utf8'),
            'password': unicode('密码', 'utf8'),
            'repassword': unicode('重复密码', 'utf8'),
            'register': unicode('免费注册', 'utf8'),
            'registerbtn': unicode('免费注册', 'utf8'),
            'loginbtn': unicode('注册', 'utf8'),
            'losepw': unicode('忘记密码', 'utf8'),  
        },
        'uiconform': {
            'title': unicode('符合', 'utf8'),
            'backbtn': unicode('起始页', 'utf8'),
        },
        'uilosepw': {
            'title': unicode('忘记密码', 'utf8'),
            'email': unicode('电邮', 'utf8'),
            'send': unicode('受密码', 'utf8'),
            'back': unicode('后面', 'utf8')
        },
        'uiprofile': {
            'title': unicode('剖面', 'utf8'),
            'changepw': unicode('更改密码', 'utf8'),
            'delaccount': unicode('删除帐号', 'utf8'),
            'logout': unicode('退出', 'utf8'),
            'headline': unicode('欢迎用户', 'utf8')
        },
        'uichangepw': {
            'title': unicode('更改密码', 'utf8'),
            'changepw': unicode('更改密码', 'utf8'),
            'delaccount': unicode('删除帐号', 'utf8'),
            'profile': unicode('剖面', 'utf8'),
            'logout': unicode('退出', 'utf8'),
            'oldpassword': unicode('老密码', 'utf8'),
            'newpassword': unicode('新密码', 'utf8'),
            'renewpassword': unicode('新密码 (重复)', 'utf8')
        },
        'uisetpw': {
            'title': unicode('集新更改密码', 'utf8'),
            'newpassword': unicode('新密码', 'utf8'),
            'renewpassword': unicode('新密码 (重复)', 'utf8'),
            'back': unicode('后面', 'utf8')
        },
        'uidelaccount': {
            'title': unicode('删除帐号', 'utf8'),
            'changepw': unicode('更改密码', 'utf8'),
            'delaccount': unicode('删除帐号', 'utf8'),
            'profile': unicode('剖面', 'utf8'),
            'delete': unicode('是的', 'utf8'),
            'logout': unicode('退出', 'utf8'),
        },
        'login': {
            'false': unicode('这是不正确的组合。', 'utf8'),
            'not active': unicode('您的帐户没有被激活。', 'utf8'),
            'unknown': unicode('这是不正确的组合。', 'utf8'),
            'empty': unicode('电子邮件字段为空。', 'utf8')
        },
        'register': {
            'not equal': unicode('密码必须是平等的。', 'utf8'),
            'not valid': unicode('电子邮件地址是无效的。', 'utf8'),
            'present': unicode('已经注册的电子邮件地址。', 'utf8'),
            'empty': unicode('电子邮件字段为空。', 'utf8'),
            'end': unicode('访问的链接，激活您的帐号，我们送你。', 'utf8')
        },
        'conform': {
            'True': unicode('您已成功激活您的帐户。', 'utf8'), 
            'False': unicode('有没有户口，可以得到激活。', 'utf8')
        },
        'losepassword': {
            'empty': unicode('未注册的电子邮件地址。', 'utf8'),
            'True': unicode('邮件已成功发送。', 'utf8')
        },
        'setpassword': {
            'not present': unicode('不存在', 'utf8'),
            'not equal': unicode('不存在', 'utf8'),
            'set': unicode('集', 'utf8'),
        },
        'changepassword': {
            'change': unicode('您的密码已被更改。', 'utf8'),
            'not equal': unicode('新密码必须是平等的。', 'utf8'),
            'wrong': unicode('你的密码并未改变。', 'utf8')
        },
        'mailsubjects': {
            'pwchange': unicode('新密码必须是平等的。', 'utf8'),
            'activate': unicode('你的密码并未改变。', 'utf8')
        }
    },
    'en' : {
        'uiindex' : {
            'title': 'GAE Users',
            'headline': 'Welcome',
            'login': 'Loginform',
            'email': 'email',
            'password': 'password',
            'repassword': 'password (repeat)',
            'register': 'Registerform',
            'registerbtn': 'Register',
            'loginbtn': 'Login',
            'losepw': 'Lose password',  
        },
        'uiconform': {
            'title': 'Conform',
            'backbtn': 'Startpage',
        },
        'uilosepw': {
            'title': 'Lose password',
            'email': 'email',
            'send': 'Get Password',
            'back': 'Back'
        },
        'uiprofile': {
            'title': 'Profile',
            'changepw': 'Change Password',
            'delaccount': 'Delete Account',
            'logout': 'Logout',
            'headline': 'Welcome User'
        },
        'uichangepw': {
            'title': 'Change Password',
            'changepw': 'Change Password',
            'delaccount': 'Delete Account',
            'profile': 'Profile',
            'logout': 'Logout',
            'oldpassword': 'old password',
            'newpassword': 'new password',
            'renewpassword': 'new password (repeat)'
        },
        'uisetpw': {
            'title': 'Set Password',
            'newpassword': 'new password',
            'renewpassword': 'new password (repeat)',
            'back': 'Back'
        },
        'uidelaccount': {
            'title': 'Delete Account',
            'changepw': 'Change Password',
            'delaccount': 'Delete Account',
            'profile': 'Profile',
            'delete': 'Yes',
            'logout': 'Logout'            
        },
        'login': {
            'false': 'This is not the right combination.',
            'not active': 'Your account is not activated.',
            'unknown': 'This is not the right combination.',
            'empty': 'The email field is empty.'
        },
        'register': {
            'not equal': 'The passwords must be equal.',
            'not valid': 'The email address is not valid.',
            'present': 'The email address is already registered.',
            'empty': 'The email field is empty.',
            'end': 'Activate your account by visiting the link, we sent you.'
        },
        'conform': {
            'True': 'You have successfully activated your account.',
            'False': 'There is no account which can get activated.'
        },
        'losepassword': {
            'empty': 'The email address is not registered.',
            'True': 'The mail has been sent successfully.'
        },
        'setpassword': {
            'not present': 'You can\'t change the password.',
            'not equal': 'New passwords must be equal.',
            'set': 'New password is stored.',
        },
        'changepassword': {
            'change': 'Your password has been changed.',
            'not equal': 'New passwords must be equal.',
            'wrong': 'Your password has not been changed.'
        },
        'mailsubjects': {
            'pwchange': 'Password change link',
            'activate': 'User registration'
        }
    }
}