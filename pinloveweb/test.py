# -*- coding: utf-8 -*-
from apps.third_party_login_app.models import ThirdPsartyLogin
from django.shortcuts import render
from apps.upload_avatar import get_uploadavatar_context
from apps.user_app.models import UserProfile
from django.http.response import HttpResponse
from django.db import transaction

@transaction.commit_on_success
def tests(request):
    UserProfile.objects.filter(user=request.user).update(guide=None)
    a=1
    a=int('sd')
    return HttpResponse('success')
    
def send_eamil_test():
    from pinloveweb.settings import DEFAULT_FROM_EMAIL
    subject, from_email, to = 'hello', DEFAULT_FROM_EMAIL, 'habfy65@gmail.com'    
    text_content = 'This is an important message.'  
    from django.template.loader import get_template
    htmly=get_template('Email_Template.html')
    from django.core.mail.message import EmailMultiAlternatives
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])  
    from django.template.context import Context
    d = Context({})
    html_content = htmly.render(d)
    msg.attach_alternative(html_content, "text/html")  
    msg.send()  
