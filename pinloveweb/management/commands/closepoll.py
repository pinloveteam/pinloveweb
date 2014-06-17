# -*- coding: utf-8 -*-
'''
Created on 2014年4月17日

@author: jin
'''
from django.core.management.base import BaseCommand
from apps.common_app.models import School
import random
from apps.user_app.models import UserProfile
from django.contrib.auth.models import User
from apps.recommend_app.models import UserExpect, Grade
class Command(BaseCommand):
    def handle(self, *args, **options):
        #生成测试数据
        school=School.objects.all()
        for i in range(1,2):
            if i>0:
                user=User(username='%s%s'%('jin',i),password='%s%s'%('jin',i))
                user.save()
                userProfile=UserProfile(user=user,gender='M',year_of_birth=random.randint(1880,1993),month_of_birth=random.randint(1,12),day_of_birth=random.randint(1,30)
               ,age=random.randint(18,33), height=random.randint(155,200),education=random.randint(0,4),
                       educationSchool=school[random.randint(1,600)].name,income=random.randint(5,100),)
            else:
                pass
            UserExpect(user_id=i,heighty1=random.randint(1,100),heighty2=random.randint(1,100),heighty3=random.randint(40,100),heighty4=random.randint(50,100),heighty5=random.randint(20,100),
                heighty6=random.randint(1,100),heighty7=random.randint(1,100),heighty8=random.randint(1,100),).save()
            
            Grade(user_id=i,heightweight=random.uniform(0,1),incomeweight=random.uniform(0,1),
            edcationscore=random.randint(0,100),edcationweight=random.uniform(0,1),appearancescore=random.uniform(30,100),appearanceweight=random.uniform(0,1),appearancesvote=random.randint(0,20)).save()
        self.stdout.write('score cache reset success!')