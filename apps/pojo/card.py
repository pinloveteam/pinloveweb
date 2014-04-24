# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''
from apps.user_app.models import UserProfile, BrowseOherScoreHistory
from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
from apps.recommend_app.models import MatchResult, Grade
from django.utils import simplejson
'''
  卡片类
'''
empty_result_list=[-1,'N',None]
class Card(object):
    def __init__(self,userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city):
        self.user_id=userId
        self.username=username
        self.height=height
        self.age=age
        self.education=education
        self.income=income
#         self.jobIndustry=jobIndustry
#         self.heighScore=heighScore
#         self.incomeScore=incomeScore
#         self.edcationScore=edcationScore
#         self.appearanceScore=appearanceScore
#         self.characterScore=characterScore
#         self.scoreOther=int(scoreOther)
#         self.scoreMyself=int(scoreMyself)
        '''
        关注情况
        0 未关注
        1 我关注
        2 相互关注
        '''
        self.followStatus=followStatus
        self.avatar_name=avatar_name
        self.isVote=isVote
        self.city=city
        
    def _dict_(self):
        dict=vars(self) 
        for key in dict.keys():
            if dict[key] in [-1,'N',None]:
                dict[key]=u'未填'
        return dict
    
'''
class 转换 simplejson
'''        
class MyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Card):
            return super(MyEncoder, self).default(obj)
        dict=obj.__dict__
        for key in dict.keys():
            if dict[key] in [-1,'N',None]:
                dict[key]=u'未填'
        if dict['age']!=u'未填':
            dict['age']=str(dict['age'])+u'岁'
        return dict
        
'''
 推荐结果MatchResultList转换CardList 卡片集合
 attribute：
    matchResultList  :  MatchResult集合
'''
def matchResultList_to_CardList(matchResultList):
    recommendResultList=[]
    for matchResult in matchResultList:
       grade=Grade.objects.get(user=matchResult.other)
       userBaiscProfile=matchResult.get_user_basic_profile()
       userId=matchResult.other_id
       username=matchResult.other.username
       height=userBaiscProfile.height
       age=userBaiscProfile.age
       education=userBaiscProfile.get_education_display()
       income=userBaiscProfile.get_income_display()
       jobIndustry=userBaiscProfile.get_jobIndustry_display()
       city=userBaiscProfile.city
       followStatus=0
       #判断头像是否通过审核
       if userBaiscProfile.avatar_name_status=='3':
           avatar_name=userBaiscProfile.avatar_name
           isVote=True
       else:
           avatar_name=DEFAULT_IMAGE_NAME
           isVote=False
       recommendResult=Card(userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city)
       recommendResultList.append(recommendResult)
    return recommendResultList
'''
将用户详细信息userProfileList转换成卡片集合CardList
attribute：
 userProfileList：  用户详细信息集合
'''
def userProfileList_to_CardList(userProfileList):
     recommendResultList=[]
     for userProfile in userProfileList:
       userId=userProfile.user_id
       username=userProfile.user.username
       height=userProfile.height
       age=userProfile.age
       education=userProfile.get_education_display()
       income=userProfile.get_income_display()
       jobIndustry=userProfile.get_jobIndustry_display()
       followStatus=0
       city=userProfile.city
       #判断头像是否通过审核
       if userProfile.avatar_name_status=='3':
           avatar_name=userProfile.avatar_name
           isVote=True
       else:
           avatar_name=DEFAULT_IMAGE_NAME
           isVote=False
       recommendResult=Card(userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city)
       recommendResultList.append(recommendResult)
     return recommendResultList
 
'''
将用户详细信息userProfileList转换成卡片集合CardList
attribute：
 userProfileList：  用户详细信息集合
''' 
def fllowList_to_CardList(user,fllowList,type):
    recommendResultList=[]
    userList=[]
    if type ==1:
        for myFollow in fllowList:
            userList.append(myFollow.follow)
    else:
        for myFollow in fllowList:
            userList.append(myFollow.my)
    userProfileList=UserProfile.objects.select_related().filter(user_id__in=userList)
    for userProfile in userProfileList:
#         #获取推荐分数
#         if  MatchResult.objects.filter(my_id=user.id,other_id=userProfile.user_id).exists():
#             matchResult=MatchResult.objects.select_related('other').get(my_id=user.id,other_id=userProfile.user_id)
#             grade=Grade.objects.get(user=matchResult.other)
#             heighScore=matchResult.heighMatchOtherScore
#             incomeScore=grade.incomescore
#             edcationScore=grade.educationscore
#             appearanceScore=grade.appearancescore
#             characterScore=matchResult.tagMatchOtherScore
#         else:
#             heighScore,incomeScore,edcationScore,appearanceScore,characterScore=0,0,0,0,0
        userId=userProfile.user_id
        username=userProfile.user.username
        height=userProfile.height
        age=userProfile.age
        education=userProfile.get_education_display()
        income=userProfile.get_income_display()
        jobIndustry=userProfile.get_jobIndustry_display()
        followStatus=0
        if userProfile.avatar_name_status=='3':
           avatar_name=userProfile.avatar_name
           isVote=True
        else:
           avatar_name=DEFAULT_IMAGE_NAME
           isVote=False
        city=userProfile.city
        recommendResult=Card(userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city)
        recommendResultList.append(recommendResult)
    return recommendResultList
 
 
    
