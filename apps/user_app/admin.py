'''
Created on Jul 4, 2013

@author: jin
'''
from django.contrib import admin
from models import User,Message,Friend,new
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(new)
