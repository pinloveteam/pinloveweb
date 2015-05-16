# -*- coding: utf-8 -*-
from apps.third_party_login_app.models import ThirdPsartyLogin
from django.shortcuts import render
from apps.upload_avatar import get_uploadavatar_context
from apps.user_app.models import UserProfile
from django.http.response import HttpResponse
from django.db import transaction
from util.email import Email
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.utils import simplejson
import time

@transaction.commit_on_success
def tests(request):
    time.sleep(2)
    return HttpResponse('success')
#     from apps.weixin_app.forms import InfoForm
#     userProfile=UserProfile.objects.get(user_id=5)
#     infoForm=InfoForm(instance=userProfile)
#     return render(request,'test.html',{'infoForm':infoForm})
#     from apps.task_app.email import send_notify_email
#     args=send_notify_email(userIdList=[54,3])
#     return  render(request,'Email_Template.html',args)
#     if request.GET.get('type')  is not None:
#         email=Email('jin521436@163.com','jin')
#         email.send(from_addr='pinloveteam@pinlove.com')
#     else:
#         email = EmailMessage('tsest', 'test', 'pinloveteam@pinlove.com', ['jin521436@163.com'])
#         email.send()
# 
#     return HttpResponse('success')
 
    
def uodate_recommend(request):
    from django.core.cache import cache
    recommend=cache.get('HAS_RECOMMEND')
    for key in recommend.keys():
        result=recommend[key]
        fieldList=['userExpect','weight','tag','info',"avatar"]
        for field in fieldList:
            from util.cache import has_recommend
            has_recommend(key,field)
    recommend=cache.get('HAS_RECOMMEND')
    for key in recommend.keys():
        recommend[key].pop('grade')
    cache.set('HAS_RECOMMEND',recommend)
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


def jsonp(request):
    if 'callback' in request.REQUEST:
        # a jsonp response!
        data = { 
'name':'sdsd', 
'gendar':'F', 
} 
        data = '%s(%s);' % (request.REQUEST['callback'], simplejson.dumps(data))
        return HttpResponse(data, "text/javascript")