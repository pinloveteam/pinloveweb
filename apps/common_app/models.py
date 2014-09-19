# -*- coding: utf-8 -*-
'''
Created on Sep 24, 2013

@author: jin
'''
from django.db import models
import datetime
class School(models.Model):
    ranking=models.SmallIntegerField(verbose_name=r'大学排名',null=True)
    name=models.CharField(verbose_name=r'大学名字',max_length=50,null=True)
    """
       类型 分为博士，硕士，本科:1，专科:2
    """
    SCHOOL_TYPE_CHOICE=(('1',u'国内985，美国前50'),('2',u'国内重点，美国前 200'),('3',u'国内本科，美国前500'),
                 ('4',u'国内民办本科，美国前1000'),)
    type=models.CharField(verbose_name=r'大学类型',max_length=2,choices=SCHOOL_TYPE_CHOICE,null=True)
    SCHOOL_COUNTRY_CHOICE=(('1',u'中国'),('2',u'美国'),)
    country=models.CharField(verbose_name=r'大学国家',max_length=2,choices=SCHOOL_COUNTRY_CHOICE,null=True)
    class Meta:
        verbose_name = u'学校' 
        verbose_name_plural = u'学校'
        db_table = "school" 

class AreaManager(models.Manager):
    def get_country_list(self):
        areaList=Area.objects.filter(area_level=0,status=1)
        return [[area.area_id,area.area_name] for area in areaList]
'''
地区
'''
class Area(models.Model):
    area_id=models.CharField(max_length=11,verbose_name=u'区域编号',primary_key=True)
    area_name=models.CharField(max_length=50,verbose_name=u'地区名称')
    parent=models.ForeignKey("self",verbose_name=u'父级编号')
    AREA_LEVEL_CHOICES=((0,u'国'),(1,u'省'),(2,u'市'),(3,u'区县'))
    area_level=models.SmallIntegerField(verbose_name=u'区域等级',choices=AREA_LEVEL_CHOICES)
    STATUS_CHOICES=((1,u'可用'),(0,u'不可用'))
    status=models.CharField(max_length=2,verbose_name=u'状态',choices=STATUS_CHOICES)
    #定制管理器
    objects = AreaManager()
    class Meta:
        verbose_name = u'地区表' 
        verbose_name_plural = u'地区表'
        db_table = "area" 
'''
标签表
'''
class Tag(models.Model):
    content=models.CharField(max_length=25,verbose_name=u'标签内容')
    #用于区分一组对立性格，例如：内向外向的对立
    group=models.SmallIntegerField(verbose_name=u'性格分组')
    value=models.SmallIntegerField(verbose_name=u'性格标签的值')
    class Meta:
        verbose_name = u'标签表' 
        verbose_name_plural = u'标签表'
        ordering = ['group','value']
        db_table = "tag" 
        
'''
缓存备份表
'''        
class BackupCache(models.Model):
    GIRLS=models.TextField(verbose_name=r'拼图匹配女生',blank=True, null=True,)
    BOYS=models.TextField(verbose_name=r'拼图匹配男生',blank=True, null=True,)
    USER_GAME_COUNT=models.TextField(verbose_name=r'免费剩余次数',blank=True, null=True,)
    USER_GAME_COUNT_FOREVE=models.TextField(verbose_name=r'永久次数',blank=True, null=True,)
    INVITE_COUNT=models.TextField(verbose_name=r'邀请成功次数(<3)',blank=True, null=True,)
    CONFIRM_INVITE=models.TextField(verbose_name=r'回应邀请用户',blank=True, null=True,)
    backupTime=models.DateTimeField(verbose_name=r'备份时间',default=datetime.datetime.today(),)
    class Meta:
        verbose_name = u'备份表' 
        verbose_name_plural = u'备份表'
        db_table = "backup_cache" 