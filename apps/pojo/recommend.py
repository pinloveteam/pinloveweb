# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''
from django.utils import simplejson
from apps.recommend_app.models import Grade
'''
  推荐结果类
'''
empty_result_list=[-1,'N',None]
class RecommendResult(object):
    def __init__(self,*args,**kwargs):
        if not kwargs.get('kwargs',None) is None:
            kwargs=kwargs.get('kwargs')
        self.userId=kwargs.pop('user_id',None)
        grade=Grade.objects.get(user_id=self.userId)
        self.incomeScore=grade.incomescore
        self.edcationScore=grade.educationscore
        self.appearanceScore=grade.appearancescore
        self.heighScore=kwargs.pop('heighMatchOtherScore',None)
        self.characterScore=kwargs.pop('tagMatchOtherScore',None)
        self.scoreMyself=int(kwargs.pop('scoreMyself',None))
        self.scoreOther=int(kwargs.pop('scoreOther',None))
     
    '''
    转换成字典类型，如果fields=None，则全部转换
    '''   
    def get_dict(self,isPermission=False):
        if isPermission:
            return self.__dict__
        else:
            args={}
            fields=['incomeScore','edcationScore','appearanceScore','heighScore','characterScore','scoreOther']
            for field in fields:
                args[field]=getattr(self,field)
            return args
        
    '''
    判断是否有权限查看scoreMyself
    '''
    def is_permission(self,userId=None):
        from apps.user_app.models import UserProfile
        member=UserProfile.objects.get(user_id=userId).member
        if member>0:
            return True
        else:
            from apps.user_app.models import BrowseOherScoreHistory
            if BrowseOherScoreHistory.objects.filter(my_id=userId,other_id=self.userId).exists():
                return True
        return False
                
       
def  MarchResult_to_RecommendResult(marchResult):
    return RecommendResult(user_id=marchResult.other_id,heighMatchOtherScore=marchResult.heighMatchOtherScore,
                           tagMatchOtherScore=marchResult.tagMatchOtherScore,scoreMyself=marchResult.scoreMyself,
                           scoreOther=marchResult.scoreOther)
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