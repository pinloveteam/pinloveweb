# -*- coding: utf-8 -*-
'''
Created on Sep 5, 2013

@author: jin
'''
from django.contrib.auth.models import User
from apps.recommend_app.models import Grade, UserExpect
import MySQLdb
from pinloveweb import settings

""""
根据用户id，相貌打分计算最终相貌分数
attribute：id ：用户id  int
           voteSocre: 相貌打分分数 int
return:   最终相貌分数
"""
def cal_looks(id,voteSocre):
    try:
        geadeInstance=Grade.objects.get(user_id=id)
    except Grade.DoesNotExist:
        print '根据id:'+id+'没有对应的grade'
        pass
    return (geadeInstance.appearancescore*(geadeInstance.appearancesvote)+voteSocre)/(geadeInstance.appearancesvote+1)
"""
根据用户收入计算用户收入分数
attribute ：
      user_income  用户收入 ：int
returns:
      收入得分
"""
def cal_income(user_income):
    from apps.user_app.models import UserProfile
    overIncomeCount=UserProfile.objects.filter(income__gte=user_income).count()+0.00
    IncomeCount=User.objects.count()
#     print str(overIncomeCount)+" "+str(IncomeCount)
    return (overIncomeCount/IncomeCount)*100
'''
根据学历，学校计算分数
attribute：
      user_education : 学历 int
      school ：学校名字  string
return：
      score：学历分数
'''
def cal_education(user_education,school):
    from apps.user_app.models import  School
    educationTupe=(90,80,70,60,40,20)
    schoolTupe=(85,75,60,40,30)
    educationMap={'master':5,'doctor':10}
    if school.strip()=='' and user_education!=-1:
        return schoolTupe[4-user_education]
    if  school.strip()!='':
        count=School.objects.filter(name=school).count()
        if count==0 :
            if user_education==-1:
                return 40
            else:
                return schoolTupe[4-user_education]
        else :
            school=School.objects.get(name=school)
            if user_education==-1:
                return educationTupe[int(school.type)-1]
            else:
                score=schoolTupe[int(school.type)-1]
                if user_education==3:
                    score+=educationMap.get('master')
                if user_education==4:
                    score+=educationMap.get('doctor')
                return score
'''
相用户貌投票
'''
def cal_user_vote(score,geadeInstance):
     
     return (geadeInstance.appearancescore*100+score*(geadeInstance.appearancesvote+1))/(100+geadeInstance.appearancesvote)
 
def cal_recommend(userId):
    from apps.user_app.models import UserProfile
    if UserExpect.objects.filter(user_id=userId).exists() and  Grade.objects.filter(user_id=userId).exists(): 
            if  not (UserProfile.objects.filter(user_id=userId).filter(height=-1).exists() )and not (UserExpect.objects.filter(user_id=userId).filter(heighty1=0.00).filter(heighty2=0.00).filter(heighty3=0.00).exclude(heighty4=0.00).filter(heighty5=0.00).filter(heighty6=0.00).filter(heighty7=0.00).filter(heighty8=0.00).exists()) and \
           Grade.objects.filter(user_id=101).exclude(heightweight__isnull=True).exclude(incomescore__isnull=True).exclude(incomeweight__isnull=True).exclude(edcationscore__isnull=True).exclude(edcationweight__isnull=True).exclude(appearancescore__isnull=True).exclude(appearanceweight__isnull=True).exists():
               connection = MySQLdb.connect(user=settings.DATABASES['default']['USER'],
                                          db=settings.DATABASES['default']['NAME'], passwd=settings.DATABASES['default']['PASSWORD'], host=settings.DATABASES['default']['HOST'])
               cursor=connection.cursor();
               r=cursor.callproc('recommend',[userId,])
               connection.commit()
               cursor.close()