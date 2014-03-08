# -*- coding: utf-8 -*-
'''
Created on 2014年1月8日

@author: jin
'''
from django.core.mail import send_mail
from util_settings import domain_name
'''
发送注册短信
'''
def send_register_email(user,user_code):
     email_verification_link = domain_name + '?username=' + user.username + '&' + 'user_code=' + user_code
     email_message = u"请您点击下面这个链接修改密码："
     email_message += email_verification_link
     send_mail(u'拼爱网，密码找回', email_message,'pinloveteam@pinpinlove.com',[user.email])
