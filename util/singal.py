# -*- coding: utf-8 -*-
'''
Created on Sep 20, 2013

@author: jin
'''
import django.dispatch
'''
用于计算推荐算法
attribute：
   
'''
cal_recommend_user = django.dispatch.Signal(providing_args=['userProfile','height','education','educationSchool','income'])
cal_recommend_grade = django.dispatch.Signal(providing_args=[])
