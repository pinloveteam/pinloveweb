# coding: utf-8 
'''
Created on 2014年1月9日

@author: jin
'''
import MySQLdb
from apps.common_app.models import School
from django.contrib.auth.models import User
import random
from apps.user_app.models import UserProfile
from apps.recommend_app.models import UserExpect, Grade
from django.utils.timezone import now

connection = MySQLdb.connect(user='root', db='django', passwd='jin521436', host='localhost')
cursor=connection.cursor();
start = now()

    
school=School.objects.all()
# user=UserProfile(user_id=1,gender='M',year_of_birth=random.randint(1880,1993),month_of_birth=random.randint(1,12),day_of_birth=random.randint(1,30)
#             ,age=random.randint(18,33), height=random.randint(155,200),education=random.randint(0,4),
#                        educationSchool=school[random.randint(1,600)].name,income=random.randint(5,100),)
# user.cal_age()
# user.save()
# UserExpect(user_id=1,heighty1=random.randint(1,100),heighty2=random.randint(1,100),heighty3=random.randint(1,100),heighty4=random.randint(1,100),heighty5=random.randint(1,100),
#                 heighty6=random.randint(1,100),heighty7=random.randint(1,100),heighty8=random.randint(1,100),).save()
# g=Grade(user_id=1,heightweight=random.uniform(0,1),incomescore=random.uniform(0,100),incomeweight=random.uniform(0,1),
#             edcationscore=random.randint(0,100),edcationweight=random.uniform(0,1),appearancescore=random.uniform(0,100),appearanceweight=random.uniform(0,1),appearancesvote=random.randint(0,20)).save()
for i in range(2,20):
    user1=User(username=str(i),)
    user1.set_password('112233')
    user1.save()
    if i>10:
       user=UserProfile(user_id=i,gender='M',year_of_birth=random.randint(1880,1993),month_of_birth=random.randint(1,12),day_of_birth=random.randint(1,30)
            ,age=random.randint(18,33), height=random.randint(155,200),education=random.randint(0,4),
                       educationSchool=school[random.randint(1,600)].name,income=random.randint(5,100),)
   
    else:
         user=UserProfile(user_id=i,gender='F',year_of_birth=random.randint(1880,1993),month_of_birth=random.randint(1,12),day_of_birth=random.randint(1,30)
            ,age=random.randint(18,33), height=random.randint(155,200),education=random.randint(0,4),
                       educationSchool=school[random.randint(1,600)].name,income=random.randint(5,100),)
    user.cal_age()
    user.save()
    
    UserExpect(user_id=i,heighty1=random.randint(1,100),heighty2=random.randint(1,100),heighty3=random.randint(1,100),heighty4=random.randint(1,100),heighty5=random.randint(1,100),
                heighty6=random.randint(1,100),heighty7=random.randint(1,100),heighty8=random.randint(1,100),).save()
    g=Grade(user_id=i,heightweight=random.uniform(0,1),incomescore=random.uniform(0,100),incomeweight=random.uniform(0,1),
            edcationscore=random.randint(0,100),edcationweight=random.uniform(0,1),appearancescore=random.uniform(0,100),appearanceweight=random.uniform(0,1),appearancesvote=random.randint(0,20)).save()

# if  Grade.objects.filter(user_id=101).exclude(heightweight__isnull=True).exclude(incomescore__isnull=True).exclude(incomeweight__isnull=True).exclude(edcationscore__isnull=True).exclude(edcationweight__isnull=True).\
# exclude(appearancescore__isnull=True).exclude(appearanceweight__isnull=True).exists():
# if not UserExpect.objects.filter(user_id=101).filter(heighty1=0.00).filter(heighty2=0.00).filter(heighty3=0.00).filter(heighty4=0.00).filter(heighty5=0.00).filter(heighty6=0.00).filter(heighty7=0.00).filter(heighty8=0.00).exists():
#  print 00
# else:
#  print 33
# cal_recommend(101)
# userProfileList=UserProfile.objects.exclude(user_id=3).exclude(gender='M').order_by("?")
# print userProfileList[0].user_id