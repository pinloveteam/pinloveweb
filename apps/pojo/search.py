# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''
from django.utils import simplejson
'''
  推荐结果类
'''
class SearchRsult(object):
    def __init__(self,userId,username,avatar_name,height,age,education,income,jobIndustry,sunSign=None,hasHouse=None,hasCar=None,stateProvince=None,country=None,city=None):
        self.username=username
        self.height=height
        self.age=age
        self.education=education
        self.income=income
        self.jobIndustry=jobIndustry
        self.avatar_name=avatar_name
        self.sunSign=sunSign
        self.hasHouse=hasHouse
        self.hasCar=hasCar
        self.stateProvince=stateProvince
        self.country =country
        self.city=city
        if self.jobIndustry==None:
            self.jobIndustry='未填'
        if self.hasHouse==None:
            self.hasHouse='未填'
        if self.hasHouse==None:
            self.jobIndustry='未填'
        if self.hasCar==None:
            self.hasCar='未填'
        if self.sunSign==None:
            self.sunSign='未填'
        
class SearchRsultEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, SearchRsult):
            return super(SearchRsultEncoder, self).default(obj)
        dict=obj.__dict__
        return dict