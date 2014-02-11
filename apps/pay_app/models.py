# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
model ThirdPsartyLogin 第三方登录表
'''
from django.db import models
from django.contrib.auth.models import User
 
class FacebookPayDetail(models.Model):
    id=models.CharField(verbose_name=u'支付ID',primary_key=True,max_length=125)
    amount=models.DecimalField(verbose_name=u'支付金额',max_digits=5, decimal_places=2)
    currency=models.CharField(verbose_name="货币类型",max_length=10)   
    quantity=models.IntegerField(verbose_name=u'购买金额')
    status=models.CharField(verbose_name=u'交易装填',max_length=10)
    signed_request=models.TextField(verbose_name=u'交易详细信息')
    class Meta:
        verbose_name = u'facebook交易明细表' 
        verbose_name_plural = u'facebook交易明细表'
        db_table = "facebook_pay_detail" 