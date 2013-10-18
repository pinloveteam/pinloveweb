'''
Created on Jul 4, 2013

@author: jin
'''
#-*- coding: utf-8 -*-
from django.contrib import admin
from apps.publish_app.models import Publish
from pinloveweb.settings import STATIC_URL
import time
import datetime

class PublishAdmin(admin.ModelAdmin):
    list_display = ('title','publishDate',)
    fields =('title','picture','content','applyChannel')
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.publishDate=datetime.datetime.today()
        obj.save()
    class Media:
        js = (
                 STATIC_URL+'js/tiny_mce/tiny_mce.js',
                 STATIC_URL+'js/textareas.js',
             )
               
admin.site.register(Publish,PublishAdmin)