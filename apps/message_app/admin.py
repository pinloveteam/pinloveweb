# #-*- coding: utf-8 -*-
# '''
# Created on Jul 4, 2013
# 
# @author: jin
# '''
# from django.contrib import admin
# from pinloveweb.settings import STATIC_URL, DEFAULT_FROM_EMAIL
# import datetime
# from django.db import models, connection
# from django import forms
# from util.form_util import HorizRadioRenderer
# from django.core.mail import send_mass_mail
# from django.core.mail.message import EmailMultiAlternatives
# from apps.message_app.models import Notify
# 
# 
# class NotifyAdminForm(forms.ModelForm):
#     class Meta:
#         model = Notify
#         widgets = {
#           'type':forms.RadioSelect(renderer=HorizRadioRenderer,)
#         }
#             
# class NotifyAdmin(admin.ModelAdmin):
#     list_display = ('type','title',)
#     fields = ('type','title','content')
#     """
#     重写保存
#     type 为 0 为系统消息
#     type 为1 为系统邮件，发邮件
#     """
#     def save_model(self, request, obj, form, change):
#         from django.contrib.auth.models import User
#         userList=User.objects.all()
#         if obj.type=='0':
# #             list=[]
# #             obj.send = request.user
# #             obj.sendTime=datetime.datetime.today()
#             cursor=connection.cursor();
#             r=cursor.callproc('BatchInsertNotify',[obj.type,request.user.id,obj.title,obj.content,])
#             connection.commit()
#             cursor.close()
#         else:
#             content="<thml><head></head><body>"+obj.content+"</body></thml>"
#             subject, from_email=obj.title,DEFAULT_FROM_EMAIL
#             mailList=[]
#             for user in userList:
#                 if user.email.strip()!='':
#                     mailList.append(user.email)
# #             message=(subject, from_email, to,mailList)
# #             send_mass_mail((message,),fail_silently=False)
#             msg = EmailMultiAlternatives(subject, content, from_email, mailList)
#             msg.attach_alternative(content, "text/html")
#             msg.send()
#             obj.sender = request.user
#             obj.sendTime=datetime.datetime.today()
#             obj.save()    
#   
#         
#     form = NotifyAdminForm
#     class Media:
#         js = (
#                  STATIC_URL+'js/tiny_mce/tiny_mce.js',
#                  STATIC_URL+'js/textareas.js',
#              )
#         
#                
# admin.site.register(Notify,NotifyAdmin)