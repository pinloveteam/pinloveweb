# -*- coding: utf-8 -*-
'''
Created on Sep 24, 2013

@author: jin
'''
from django.db import models
class School(models.Model):
    ranking=models.SmallIntegerField(verbose_name=r'大学排名',null=True)
    name=models.CharField(verbose_name=r'大学名字',max_length=50,null=True)
    """
       类型 分为博士，硕士，本科:1，专科:2
    """
    SCHOOL_TYPE_CHOICE=(('1',u'国内985，美国前50'),('2',u'国内重点，美国前 200'),('3',u'国内本科，美国前500'),
                 ('4',u'国内民办本科，美国前1000'),)
    type=models.CharField(verbose_name=r'大学类型',max_length=2,choices=SCHOOL_TYPE_CHOICE,null=True)
    class Meta:
        verbose_name = u'学校' 
        verbose_name_plural = u'关注表'
        db_table = "school" 