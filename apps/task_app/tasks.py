# -*- coding: utf-8 -*-
from apps.user_app.models import UserProfile

'''
计算收入
'''
def cal_income_task():
    userProfileList=UserProfile.objects.exclude(income=-1)
    for userProfile in userProfileList:
        from apps.recommend_app.recommend_util import cal_income
        cal_income(userProfile.income,userProfile.gender)