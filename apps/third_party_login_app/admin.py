# -*- coding: utf-8 -*-
'''
Created on 2014年11月23日

@author: jin
'''
from django.contrib import admin
from apps.third_party_login_app.models import ThirdPsartyLogin

        
class ThirdPsartyLoginAdmin(admin.ModelAdmin):
    list_display=('user','provider','uid',)
    fields =('user','provider','uid','access_token','data')
    list_filter=('provider',)
    search_fields =('user__username','uid')
      

admin.site.register(ThirdPsartyLogin,ThirdPsartyLoginAdmin)
