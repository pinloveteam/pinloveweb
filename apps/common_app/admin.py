#-*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''

from django.contrib import admin
from apps.common_app.models import School
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('ranking', 'name', 'type', )

    search_fields = ('name',)
#     filter_horizontal = ('user',)  ManyToManyField
    list_filter = ('type',)

# admin.site.register(School,SchoolAdmin)


