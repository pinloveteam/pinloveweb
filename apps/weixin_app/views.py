# -*- coding: utf-8 -*-
'''
Created on 2014年5月23日

@author: jin
'''
from django.http.response import HttpResponse

def vaild(request):
    echostr=request.GET.get('echostr')
    return HttpResponse(echostr)