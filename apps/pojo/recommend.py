# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''
import simplejson
'''
  推荐结果类
'''
empty_result_list=[-1,'N',None]
class RecommendResult(object):
    def __init__(self,userId,username,avatar_name,height,age,education,income,jobIndustry,scoreOther,scoreMyself,macthScore,isFriend,isVote,city):
        self.user_id=userId
        self.username=username
        self.height=height
        self.age=age
        self.education=education
        self.income=income
        self.jobIndustry=jobIndustry
        self.scoreOther=scoreOther
        self.scoreMyself=scoreMyself
        self.macthScore=macthScore
        self.isFriend=isFriend
        self.avatar_name=avatar_name
        self.isVote=isVote
        self.city=city
        
    def _dict_(self):
        dict=vars(self) 
        for key in dict.keys():
            if dict[key] in [-1,'N',None]:
                dict[key]=u'未填'
        return dict
        
class MyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, RecommendResult):
            return super(MyEncoder, self).default(obj)
        dict=obj.__dict__
        for key in dict.keys():
            if dict[key] in [-1,'N',None]:
                dict[key]=u'未填'
        if dict['age']!=u'未填':
            dict['age']=str(dict['age'])+u'岁'
        return dict