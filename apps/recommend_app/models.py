# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save
import datetime

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
    incomescore=models.FloatField(verbose_name=u"收入分数",null=True,default='0',)
    incomeweight=models.FloatField(verbose_name=u"收入权重",null=True)
    educationscore=models.FloatField(verbose_name=u"学历分数",null=True,default='0',)
    educationweight=models.FloatField(verbose_name=u"学历权重",null=True)
    appearancescore=models.FloatField(verbose_name=u"外貌分数",null=True,default='0',)
    sysappearancescore=models.FloatField(verbose_name=u"系统外貌分数",null=True)
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
            from apps.user_score_app.method import get_score_by_height_score
            get_score_by_height_score(user_id)
            UserExpect(user_id=user_id,*args,**kwargs).save()
class UserExpect(models.Model):
    user=models.ForeignKey(User,related_name='User')
#     heightx1=models.SmallIntegerField(verbose_name=u'身高',default='160',null=True)
    heighty1=models.FloatField(verbose_name=u'160y轴分数',default='0.00',null=True)
#     heightx2=models.SmallIntegerField(verbose_name=u'身高',default='165',null=True)
    heighty2=models.FloatField(verbose_name=u'165y轴分数',default='0.00',null=True)
#     heightx3=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty3=models.FloatField(verbose_name=u'170y轴分数',default='0.00',null=True)
#     heightx4=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty4=models.FloatField(verbose_name=u'175y轴分数',default='0.00',null=True)
#     heightx5=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty5=models.FloatField(verbose_name=u'180y轴分数',default='0.00',null=True)
#     heightx6=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty6=models.FloatField(verbose_name=u'185y轴分数',default='0.00',null=True)
#     heightx7=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty7=models.FloatField(verbose_name=u'190y轴分数',default='0.00',null=True)
#     heightx8=models.SmallIntegerField(verbose_name=u'身高',default='0',null=True)
    heighty8=models.FloatField(verbose_name=u'195y轴分数',default='0.00',null=True)
    objects=UserExpectManager()
    class Meta:
        verbose_name = u'用户期望表' 
        verbose_name_plural = u'用户期望表'
        db_table=u'recommend_user_expect'
        
class MatchResultManager(models.Manager):
    '''
    根据id判断是否存在
    '''
    def is_exist_by_userid(self,myId):
        return MatchResult.objects.filter(my_id=myId).exists()
    '''
    获取匹配结果信息
    @param userId:用户id
    @param disLikeUserIdList:不喜欢用户列表 
    @param STAFF_MEMBERS：管理员列表 
    '''
    def get_match_result_by_userid(self,userId,disLikeUserIdList):
        from pinloveweb import STAFF_MEMBERS
        excludeList=[userId,]
        excludeList.extend(STAFF_MEMBERS)
        if not disLikeUserIdList is None:
            excludeList.extend(disLikeUserIdList)
        sql='''
        select u1.*,u2.* from recommend_match_result u1 
left  JOIN auth_user u2 on u2.id=u1.other_id 
LEFT JOIN  user_profile u3 on u1.other_id =u3.user_id
where u3.avatar_name_status='3' and u1.my_id=%s '''
        if len(excludeList)>1:
            sql='%s%s%s%s'%(sql,'and  u1.other_id not in (',('%s,'*(len(excludeList)-1))[:-1],')')
        return MatchResult.objects.raw(sql,excludeList)
       
       
class MatchResult(models.Model):
    my=models.ForeignKey(User,related_name='my_User',verbose_name=u"自己")
    other=models.ForeignKey(User,related_name='other_User',verbose_name=u"异性")
    scoreMyself=models.FloatField(verbose_name=u"异性给自己打分",default='0.00')
    scoreOther=models.FloatField(verbose_name=u"自己给异性打分",default='0.00')
    macthScore=models.FloatField(verbose_name=u"总分",default='0.00')
    heighMatchOther=models.FloatField(verbose_name=u"对别人身高打分",default='0.00')
    heighMatchMy=models.FloatField(verbose_name=u"对自己身高打分",default='0.00')
    incomeMatchMy=models.FloatField(verbose_name=u"对自己收入打分",default='0.00')
    incomeMatchOther=models.FloatField(verbose_name=u"对别人收入打分",default='0.00')
    edcationMatchOther=models.FloatField(verbose_name=u"对别人学历打分",default='0.00')
    edcationMatchMy=models.FloatField(verbose_name=u"对自己学历打分",default='0.00')
    appearanceMatchOther=models.FloatField(verbose_name=u"对别人外貌打分",default='0.00')
    appearanceMatchMy=models.FloatField(verbose_name=u"对自己外貌打分",default='0.00')
    characterMatchOther=models.FloatField(verbose_name=u"对别人性格打分",default='0.00')
    characterMatchMy=models.FloatField(verbose_name=u"对自己性格打分",default='0.00')
    #以下不加权重得分
    tagMatchOtherScore=models.FloatField(verbose_name=u"对异性标签匹配得分(无权重)",default='0.00')
    tagMatchMyScore=models.FloatField(verbose_name=u"异性对自己标签匹配得分(无权重)",default='0.00')
    heighMatchOtherScore=models.FloatField(verbose_name=u"异性对自己身高匹配得分(无权重)",default='0.00')
    heighMatchMyScore=models.FloatField(verbose_name=u"异性对自己身高匹配得分(无权重)",default='0.00')
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

'''
投票记录表
'''
class AppearanceVoteRecord(models.Model):
    user=models.ForeignKey(User,related_name='vote_user',verbose_name=u"打分的用户")
    other=models.ForeignKey(User,related_name='voted_user',verbose_name=u"被打分的用户")
    score=models.IntegerField(verbose_name=u"用户打分",null=True,blank=True)
    time=models.DateTimeField(verbose_name=u'创建时间',)
    def save(self, *args, **kwargs):
        self.time=datetime.datetime.now()
        super(AppearanceVoteRecord, self).save(*args, **kwargs)
    class Meta:
        verbose_name = u'投票记录表' 
        verbose_name_plural = u'投票记录表'
        db_table=u'appearance_vote_record'
    
'''
不推荐用户
'''
class NotRecommendUser(models.Model):
    my=models.ForeignKey(User,related_name='not_recommend_user_id',verbose_name=u'用户id')
    other=models.ForeignKey(User,related_name='not_recommend_other_id',verbose_name=u'不推荐用户用户')
    createTime=models.DateTimeField(verbose_name=u'创建时间',)
    
    def save(self,*args,**kwargs):
        self.createTime=datetime.datetime.now()
        super(NotRecommendUser,self).save(*args,**kwargs)
    class Meta:
        verbose_name=u'不推荐用户'
        verbose_name_plural = u'不推荐用户'
        db_table='not_recommend_user'
'''
星星权重
'''     
class WeightStar(models.Model):
    user=models.ForeignKey(User)
    CHOICE=((0,'0星'),(1,'1星'),(2,'2星'),(3,'3星'),(4,'4星'),(5,'5星'),)
    height=models.IntegerField(verbose_name=u"身高权重",choices=CHOICE,default=0)
    income=models.IntegerField(verbose_name=u"收入分数",choices=CHOICE,default=0)
    education=models.IntegerField(verbose_name=u"学历分数",choices=CHOICE,default=0)
    appearance=models.IntegerField(verbose_name=u"外貌分数",choices=CHOICE,default=0)
    character=models.IntegerField(verbose_name=u"性格权重",choices=CHOICE,default=0)
    
    def save(self,*args,**kwargs):
        if Grade.objects.filter(user=self.user).exists():
            grade=Grade.objects.get(user=self.user)
        else:
            grade=Grade(user=self.user)
        fieldList=['height','income','education','appearance','character']
        sum,avg=0,0
        for field in fieldList:
            sum+=getattr(self,field)
        avg=100.00/sum
        for field in fieldList:
            setattr( grade,field+'weight',avg*getattr(self,field))
        grade.save()
        super(WeightStar,self).save(*args,**kwargs)
    class Meta:
        verbose_name = u'权重星星' 
        verbose_name_plural = u'权重星星'
        db_table=u'weight_star'
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
