# -*- coding: utf-8 -*-
'''
Created on 2014年1月8日

@author: jin
'''
from django.core.mail import send_mail
from util_settings import domain_name
from django.core.mail.message import EmailMultiAlternatives
from pinloveweb import settings
from django.template.loader import render_to_string
'''
发送注册短信
'''
def send_register_email(user,user_code):
     email_verification_link = domain_name + '?username=' + user.username + '&' + 'user_code=' + user_code
     email_message = u"请您点击下面这个链接修改密码："
     email_message += email_verification_link
     send_mail(u'拼爱网，密码找回', email_message,'pinloveteam@pinpinlove.com',[user.email])
     
     

class TemplateEmail(object):
    '''
    发送模板邮件
    '''
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None

    def _render(self, template, context):
        return render_to_string(template, context)

    def html(self, template, context):
        self._html = self._render(template, context)

    def text(self, template, context):
        self._text = self._render(template, context)

    def send(self, from_addr=None, fail_silently=False):
        if isinstance(self.to, basestring):
            self.to = [self.to]
        if not from_addr:
            from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL')
        msg = EmailMultiAlternatives(
            self.subject,
            self._text,
            from_addr,
            self.to
        )
        if self._html:
            msg.attach_alternative(self._html, 'text/html')
        msg.send(fail_silently)