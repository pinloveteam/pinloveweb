# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from django.core.exceptions import ImproperlyConfigured
from django.db.models import signals

import MySQLdb
from pinloveweb import settings

class Grade(models.Model):
    user=models.ForeignKey(User)
    #1.height,2.income,3.edcation ,4.appearance
#     type=models.SmallIntegerField(max_length=2)
#     heightscore=models.FloatField(verbose_name=u"身高分数",default='0.00',null=True)
    heightweight=models.FloatField(verbose_name=u"身高权重",null=True)
    incomescore=models.FloatField(verbose_name=u"收入分数",null=True)
    incomeweight=models.FloatField(verbose_name=u"收入权重",null=True)
    edcationscore=models.FloatField(verbose_name=u"学历分数",null=True)
    edcationweight=models.FloatField(verbose_name=u"学历权重",null=True)
    appearancescore=models.FloatField(verbose_name=u"外貌分数",null=True)
    appearanceweight=models.FloatField(verbose_name=u"外貌权重",null=True)
    characterweight=models.FloatField(verbose_name=u"性格权重",null=True)
    appearancesvote=models.IntegerField(verbose_name=u'相貌投票数',default='0',null=True)
    class Meta:
        verbose_name = u'推荐打分表' 
        verbose_name_plural = u'推荐打分表'

'''
用户期望数据
'''  
class UserExpect(models.Model):
    user=models.ForeignKey(User,related_name='User')
#     heightx1=models.SmallIntegerField(verbose_name=u'身高',default='160',null=True)
    heighty1=models.FloatField(verbose_name=u'y1分数',default='0.00',null=True)
#     heightx2=models.SmallIntegerField(verbose_name=u'身高',default='165',null=True)
    heighty2=models.FloatField(verbose_name=u'y2分数',default='0.00',null=True)
#     heightx3=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty3=models.FloatField(verbose_name=u'y3分数',default='0.00',null=True)
#     heightx4=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty4=models.FloatField(verbose_name=u'y4分数',default='0.00',null=True)
#     heightx5=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty5=models.FloatField(verbose_name=u'y5分数',default='0.00',null=True)
#     heightx6=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty6=models.FloatField(verbose_name=u'y6分数',default='0.00',null=True)
#     heightx7=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty7=models.FloatField(verbose_name=u'y7分数',default='0.00',null=True)
#     heightx8=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty8=models.FloatField(verbose_name=u'y18分数',default='0.00',null=True)
#     class Meta:
#         verbose_name = u'用户期望biao' 
#         verbose_name_plural = u'推荐打分表'

class MatchResult(models.Model):
    my=models.ForeignKey(User,related_name='my_User',verbose_name=u"自己")
    other=models.ForeignKey(User,related_name='other_User',verbose_name=u"异性")
    scoreMyself=models.FloatField(verbose_name=u"异性给自己打分",default='0.00')
    scoreOther=models.FloatField(verbose_name=u"自己给异性打分",default='0.00')
    macthScore=models.FloatField(verbose_name=u"计算总分",default='0.00')
    class Meta:
        verbose_name = u'推荐结果表' 
        verbose_name_plural = u'推荐结果表'

#   获取对应的用户基本信息表的信息
#   attribute：
#             none
#   return：
#           class：user_basic_profile
    def get_user_basic_profile(self):
        """
        Returns user-specific favourite for this user. Raises
        UserFavouriteNotAvailable if this User does not have a  favourite.
        """
        from apps.user_app.models import UserProfile
        if not hasattr(self, '_user_basic_profile_cache'):
            try:
                self._user_basic_profile_cache = UserProfile.objects.get(user=self.other)
                self._user_basic_profile_cache.income= self._user_basic_profile_cache.get_income_display()
                self._user_basic_profile_cache.education= self._user_basic_profile_cache.get_education_display()
                self._user_basic_profile_cache.height= self._user_basic_profile_cache.get_height_display()
            except (ImportError, ImproperlyConfigured):
                print ''
                pass
        return self._user_basic_profile_cache

#运行存储过程 （推荐算法）
#p_id 要计算推荐用户的id int
def run_procedure(p_id):
    cursor=connection.cursor();
    r=cursor.callproc('recommend',[p_id,])
    result=cursor.fetchall()
    connection.commit()
    cursor.close()
'''
触发推荐事件
'''
def cal_recommend_callback(sender,**kwargs):
     userExpect=kwargs['instance']
     from apps.recommend_app.recommend_util import cal_recommend
     cal_recommend(userExpect.user.id)
'''
监听，如果UserExpect保存就触发该事件
'''
signals.post_save.connect(cal_recommend_callback, sender=UserExpect)  
