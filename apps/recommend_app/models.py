# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save

class GradeManage(models.Manager):
    '''
     如果grade没有创建则创建一个grade
否则更新
    attribute：
      userId 用户id
              可选: field:[heightweight,incomeweight,edcationweight,appearanceweight,characterweight]
      example:heightweight=height
    '''
    def create_update_grade(self,userId,*arg,**kwargs):
        if Grade.objects.filter(user_id=userId).exists():
            Grade.objects.filter(user_id=userId).update(*arg,**kwargs)
        else:
            Grade(user_id=userId,*arg,**kwargs).save()
    
class Grade(models.Model):
    user=models.ForeignKey(User)
    #1.height,2.income,3.edcation ,4.appearance
#     type=models.SmallIntegerField(max_length=2)
#     heightscore=models.FloatField(verbose_name=u"身高分数",default='0.00',null=True)
    heightweight=models.FloatField(verbose_name=u"身高权重",null=True)
    incomescore=models.FloatField(verbose_name=u"收入分数",null=True)
    incomeweight=models.FloatField(verbose_name=u"收入权重",null=True)
    educationscore=models.FloatField(verbose_name=u"学历分数",null=True)
    educationweight=models.FloatField(verbose_name=u"学历权重",null=True)
    appearancescore=models.FloatField(verbose_name=u"外貌分数",null=True)
    appearanceweight=models.FloatField(verbose_name=u"外貌权重",null=True)
    characterweight=models.FloatField(verbose_name=u"性格权重",null=True)
    appearancesvote=models.IntegerField(verbose_name=u'相貌投票数',default='0',null=True)
    objects=GradeManage()
    class Meta:
        verbose_name = u'推荐打分表' 
        verbose_name_plural = u'推荐打分表'
        db_table=u'recommend_grade'

'''
用户期望数据
'''  
class UserExpectManager(models.Manager):
    '''
    根据userid获取期望数据
    attribute：
       userId（int）
    return
       UserExpect
    '''
    def get_user_expect_by_uid(self,userId):
        if UserExpect.objects.filter(user_id=userId).exists():
            return UserExpect.objects.get(user_id=userId)
        else:
            return None
    '''
    根据userid创建和更新
    attribute：
       userId（int）
       fields : UserExpect的所有属性
    '''
    def create_update_by_uid(self,user_id=None,*args,**kwargs):
        if UserExpect.objects.filter(user_id=user_id).exists():
            UserExpect.objects.filter(user_id=user_id).update(*args,**kwargs)
        else:
            UserExpect(user_id=user_id,*args,**kwargs).save()
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
    objects=UserExpectManager()
    class Meta:
        verbose_name = u'用户期望表' 
        verbose_name_plural = u'推荐打分表'
        db_table=u'recommend_user_expect'
        
class MatchResultManager(models.Manager):
    '''
    根据id判断是否存在
    '''
    def is_exist_by_userid(self,myId):
        return MatchResult.objects.filter(my_id=myId).exists()
       
class MatchResult(models.Model):
    my=models.ForeignKey(User,related_name='my_User',verbose_name=u"自己")
    other=models.ForeignKey(User,related_name='other_User',verbose_name=u"异性")
    scoreMyself=models.FloatField(verbose_name=u"异性给自己打分",default='0.00')
    scoreOther=models.FloatField(verbose_name=u"自己给异性打分",default='0.00')
    macthScore=models.FloatField(verbose_name=u"对别人身高打分",default='0.00')
    heighMatchOther=models.FloatField(verbose_name=u"对别人身高打分",default='0.00')
    heighMatchMy=models.FloatField(verbose_name=u"对自己身高打分",default='0.00')
    incomeMatchMy=models.FloatField(verbose_name=u"对自己打分",default='0.00')
    incomeMatchOther=models.FloatField(verbose_name=u"对别人收入打分",default='0.00')
    edcationMatchOther=models.FloatField(verbose_name=u"对别人学历打分",default='0.00')
    edcationMatchMy=models.FloatField(verbose_name=u"对自己学历打分",default='0.00')
    appearanceMatchOther=models.FloatField(verbose_name=u"对别人外貌打分",default='0.00')
    appearanceMatchMy=models.FloatField(verbose_name=u"对自己外貌打分",default='0.00')
    characterMatchOther=models.FloatField(verbose_name=u"对别人性格打分",default='0.00')
    characterMatchMy=models.FloatField(verbose_name=u"对自己性格打分",default='0.00')
     #定制管理器
    objects = MatchResultManager()
    class Meta:
        verbose_name = u'推荐结果表' 
        verbose_name_plural = u'推荐结果表'
        db_table=u'recommend_match_result'

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


# '''
# 触发推荐事件
# '''
# def cal_recommend_callback(sender,**kwargs):
#     instance=kwargs['instance']
#     from util.cache import has_recommend
#     if instance.__class__.__name__=='UserExpect':
#         has_recommend(instance.user.id,'userExpect')
#     elif instance.__class__.__name__=='Grade':
#         has_recommend(instance.user.id,'grade')
#     from apps.recommend_app.recommend_util import cal_recommend
#     cal_recommend(instance.user.id)
# '''
# 监听，如果UserExpect保存就触发该事件
# '''
# post_save.connect(cal_recommend_callback, sender=UserExpect)  
# post_save.connect(cal_recommend_callback,sender=Grade)
