# -*- coding: utf-8 -*-
'''
Created on Sep 26, 2013

@author: jin
'''
import unittest
import random
from apps.recommend_app.recommend_util import cal_education
from apps.user_app.models import UserProfile

class TestCase(unittest.TestCase):
#     userProfile=UserProfile()
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
    def setUp(self): 
        pass
    #退出清理工作  
    def tearDown(self):  
        pass    

    def testEducation(self):
#     choice=-1 #未填
#     secondary=0 #大专以下
#     junior=1  # 大专
#     Bachelor =2# 本科
#     master=3 #硕士
#     doctor=4 # 博士 
    #以学校为基准，分数表示：985，211，一般本科，民办本科，专科，专科以下
      educationTupe=(95,85,70,60,40,20)
    #学校没填以学历为标准：分数表示：博士、硕士、本科、专科、专科以下
      schoolTupe=(85,75,60,40,30)
      
      #学校未填，学历填写的情况
      self.assertEqual(cal_education(1,'  '),40,'学校未填，学历大专，出错！')
      self.assertEqual(cal_education(4,'  '),85,'学校未填，学历博士，出错！')
      
      #学校填写，学历未填的情况
      self.assertEqual(cal_education(-1,u'北京大学'), 95, '985学校：北京大学，学历未填,出错！')
      self.assertEqual(cal_education(-1,u'西北大学'), 85, '211学校：西北大学，学历未填,出错！')
      print cal_education(-1,u'哈佛大学')
      self.assertEqual(cal_education(-1,u'沈阳工业大学'), 70, '一般本科学校：沈阳工业大学，学历未填,出错！')
      self.assertEqual(cal_education(-1,u'哈佛大学'), 95, '美国前50学校：哈佛大学，学历未填,出错！')
      self.assertEqual(cal_education(-1,u'sdsfd'), 40, '乱写学校：sdsd，学历未填,出错！')
      
      #学校和学历都填写的情况
      print cal_education(3,u'北京大学')
      self.assertEqual(cal_education(3,u'北京大学'), 100, '985学校：北京大学，学历本科,出错！')
      self.assertEqual(cal_education(2,u'北京大学'), 95, '985学校：北京大学，学历硕士,出错！')
      self.assertEqual(cal_education(-1,u'沈阳工业大学'), 70, '一般本科学校：西北大学，学历未填,出错！')
      self.assertEqual(cal_education(3,u'sdsfd'), 75, '乱写学校：sdsd，学历本科,出错！')
      
        
        
''''
 education
'''
# print School.objects.filter(name='哈佛大学').count()
# print cal_education(2,'中佛罗里达大学')

if __name__=='main':
     suite1 = unittest.TestLoader().loadTestsFromTestCase(TestCase())
     suite = unittest.TestSuite([suite1,])  
     unittest.TextTestRunner(verbosity=2).run(suite)  