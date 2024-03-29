# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''

from django.utils import simplejson
from apps.friend_dynamic_app.models import Picture
from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
from apps.recommend_app.models import Grade
from apps.user_app.models import UserProfile
from pinloveweb.method import is_focus_each_other
from apps.user_app.method import is_chat
empty_result_list=[-1,'N',None]

'''
 卡片基本类
'''
class CardBase(object):
    def __init__(self,userId,username,avatar_name,height,age,education,income,jobIndustry,city,avatar_name_status='3'):
        self.user_id=userId
        self.username=username
        self.avatar_name=avatar_name
        self.height=height
        self.age=age
        self.education=education
        self.income=income
        self.jobIndustry=jobIndustry
        self.city=city
        self.avatar_name_status=avatar_name_status
        
    def limit_fileds(self,length=20):
        if  isinstance(self.city,basestring) and len(self.city.encode('gbk'))>length:
            if self.city.find(u' ')!=-1:
                self.city=self.city[:self.city.find(u' ')]
    def _dict_(self):
        dict=vars(self) 
        for key in dict.keys():
            if dict[key] in [-1,'N',None]:
                dict[key]=u'未填'
        return dict
        
'''
  web版卡片类
'''
class Card(CardBase):
    def __init__(self,userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city,avatar_name_status='3'):
        CardBase.__init__(self,userId,username,avatar_name,height,age,education,income,jobIndustry,city,avatar_name_status)
        self.pictureList=[]
        #初始化图片
        self.get_pic(0,50)

        '''
        关注情况
        0 未关注
        1 我关注
        2 相互关注
        3 关注我的
        '''
        self.followStatus=followStatus
        self.isVote=isVote
        self.isChat=False
        

        
    '''
    获取用户图片
    '''
    def get_pic(self,first,end):
        pictureList=Picture.objects.filter(user_id=self.user_id).order_by('-createTime')[first:end]
        for picture in pictureList:
            from apps.friend_dynamic_app.dynamic_settings import IMAGE_SAVE_FORMAT,thumbnails
            smailPic='%s%s%s%s%s'%(picture.picPath,'-',thumbnails[0],'.',IMAGE_SAVE_FORMAT)
            pic='%s%s%s'%(picture.picPath,'.',IMAGE_SAVE_FORMAT)
            self.pictureList.append({'description':picture.description,'pic':pic,'smailPic':smailPic,'createTime':picture.createTime.strftime("%Y-%m-%d-%H")}) 
            
    
    
class CardMobile(CardBase):  
    def __init__(self,userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city,country,avatar_name_status='3'):
        CardBase.__init__(self,userId,username,avatar_name,height,age,education,income,jobIndustry,city,avatar_name_status)
        self.country=country 
 
###################################web版的方法#################################################   
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
def matchResultList_to_CardList(myId,matchResultList):
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
       jobIndustry=userBaiscProfile.jobIndustry
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
       recommendResult.limit_fileds()
       recommendResultList.append(recommendResult)
    if len(matchResultList)>0:
        #关注情况
        recommendResultList=is_focus_each_other(myId,recommendResultList)
        #是否有聊天权限
        recommendResultList=is_chat(myId,recommendResultList,)
    return recommendResultList
'''
将用户详细信息userProfileList转换成卡片集合CardList
attribute：
 userProfileList：  用户详细信息集合
'''
def userProfileList_to_CardList(myId,userProfileList):
     recommendResultList=[]
     for userProfile in userProfileList:
       userId=userProfile.user_id
       username=userProfile.user.username
       height=userProfile.height
       age=userProfile.age
       education=userProfile.get_education_display()
       income=userProfile.get_income_display()
       jobIndustry=userProfile.jobIndustry
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
       recommendResult.limit_fileds()
       recommendResultList.append(recommendResult)
     if len(recommendResultList)>0:
        #关注情况
        recommendResultList=is_focus_each_other(myId,recommendResultList)
        #是否有聊天权限
        recommendResultList=is_chat(myId,recommendResultList,)
     return recommendResultList
 

'''
将用户详细信息userProfileList转换成卡片集合CardList
attribute：
 userProfileList：  用户详细信息集合
''' 
def fllowList_to_CardList(myId,fllowList,type):
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
        userId=userProfile.user_id
        username=userProfile.user.username
        height=userProfile.height
        age=userProfile.age
        education=userProfile.get_education_display()
        income=userProfile.get_income_display()
        jobIndustry=userProfile.jobIndustry
        followStatus=0
        if userProfile.avatar_name_status=='3':
           avatar_name=userProfile.avatar_name
           isVote=True
        elif userProfile.avatar_name_status=='1':
           avatar_name=DEFAULT_IMAGE_NAME
           isVote=False
        else:
            avatar_name=userProfile.avatar_name
            isVote=False
        city=userProfile.city
        recommendResult=Card(userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city,userProfile.avatar_name_status)
        recommendResult.limit_fileds()
        recommendResultList.append(recommendResult)
    if len(recommendResultList)>0:
        #关注情况
        recommendResultList=is_focus_each_other(myId,recommendResultList)
        #是否有聊天权限
        recommendResultList=is_chat(myId,recommendResultList,)
    return recommendResultList
 
###################################web版的方法#################################################   
class CardMobileEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, CardMobile):
            return super(MyEncoder, self).default(obj)
        dict=obj.__dict__
        for key in dict.keys():
            if dict[key] in [-1,'N',None,u'未填']:
                dict[key]=None
        if dict['age']!=None:
            dict['age']=str(dict['age'])+u'岁'
        if dict['height']!=None:
             dict['height']=str(dict['height'])+u'厘米'
        return dict
    
'''
 推荐结果MatchResultList转换CardMobileList 卡片集合
 attribute：
    matchResultList  :  MatchResult集合
'''
def matchResultList_to_CardMobileList(myId,matchResultList):
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
       jobIndustry=userBaiscProfile.jobIndustry
       city=userBaiscProfile.city
       country=userBaiscProfile.country
       followStatus=0
       #判断头像是否通过审核
       if userBaiscProfile.avatar_name_status=='3':
           avatar_name=userBaiscProfile.avatar_name
           isVote=True
       else:
           avatar_name=DEFAULT_IMAGE_NAME
           isVote=False
       recommendResult=CardMobile(userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city,country)
       recommendResult.limit_fileds()
       recommendResultList.append(recommendResult)
    return recommendResultList
 
'''
将用户详细信息userProfileList转换成卡片集合CardList
attribute：
 userProfileList：  用户详细信息集合
'''
def userProfileList_to_CardMobileList(myId,userProfileList):
     recommendResultList=[]
     for userProfile in userProfileList:
       userId=userProfile.user_id
       username=userProfile.user.username
       height=userProfile.height
       age=userProfile.age
       education=userProfile.get_education_display()
       income=userProfile.get_income_display()
       jobIndustry=userProfile.jobIndustry
       country=userProfile.country
       followStatus=0
       city=userProfile.city
       #判断头像是否通过审核
       if userProfile.avatar_name_status=='3':
           avatar_name=userProfile.avatar_name
           isVote=True
       else:
           avatar_name=DEFAULT_IMAGE_NAME
           isVote=False
       recommendResult=CardMobile(userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city,country)
       recommendResult.limit_fileds()
       recommendResultList.append(recommendResult)
     return recommendResultList
 

'''
将用户详细信息userProfileList转换成卡片集合CardList
attribute：
 userProfileList：  用户详细信息集合
''' 
def fllowList_to_CardMobileList(myId,fllowList,type):
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
        userId=userProfile.user_id
        username=userProfile.user.username
        height=userProfile.height
        age=userProfile.age
        education=userProfile.get_education_display()
        income=userProfile.get_income_display()
        jobIndustry=userProfile.jobIndustry
        country=userProfile.country
        followStatus=0
        if userProfile.avatar_name_status=='3':
           avatar_name=userProfile.avatar_name
           isVote=True
        elif userProfile.avatar_name_status=='1':
           avatar_name=DEFAULT_IMAGE_NAME
           isVote=False
        else:
            avatar_name=userProfile.avatar_name
            isVote=False
        city=userProfile.city
        recommendResult=CardMobile(userId,username,avatar_name,height,age,education,income,jobIndustry,followStatus,isVote,city,country)
        recommendResult.limit_fileds()
        recommendResultList.append(recommendResult)
    return recommendResultList 
