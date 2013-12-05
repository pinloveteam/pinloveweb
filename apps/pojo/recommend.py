# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''
'''
  推荐结果类
'''
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
