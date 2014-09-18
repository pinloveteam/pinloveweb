# -*- coding: utf-8 -*-

'''
计算收入
'''
from apps.user_app.models import UserProfile
from apps.recommend_app.models import Grade
def cal_income_task():
    userProfileList=UserProfile.objects.exclude(income=-1)
    for userProfile in userProfileList:
        from apps.recommend_app.recommend_util import cal_income
        incomescore=cal_income(userProfile.income,userProfile.gender)
        Grade.objects.filter(user_id=userProfile.user_id).update(incomescore=incomescore)