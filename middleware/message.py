# -*- coding: utf-8 -*-
'''
Created on 2014年9月2日

@author: jin
'''
from django.utils import simplejson
class  PullMessageCount(object):
    def process_response(self,request,response):
        if request.is_ajax():
            temp=simplejson.loads(response.content)
            temp['jin']=1
            response.content=simplejson.dumps(temp)
            print response
        return response
            
    def  process_view(self,request, view_func, view_args, view_kwargs):
        if not request.is_ajax():
            print request