#-*- coding: UTF-8 -*- 
'''
Created on 2014年12月23日

@author: jin
'''
from apps.common_app.models import School
from django.db.models.query_utils import Q
from django.utils import simplejson
from django.http.response import HttpResponse
def select_school(request):
    args={}
    try:
        country=int(request.GET.get('country'))
        schoolName=request.GET.get('schoolName').rstrip()
        schoolList=School.objects.filter(country=country).filter(Q(name__startswith=schoolName)|Q(name__endswith=schoolName))[:30]
        schoolNameList=[school.name for school in schoolList]
        args['result']='success'
        args['schoolList']=schoolNameList
    except  Exception as e:
        args={'result':'error','error_message':e.message}
    json=simplejson.dumps(args)
    return HttpResponse(json)
        