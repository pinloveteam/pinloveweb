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
 
'''
交易表
'''       
class Charge(models.Model):
    vailAmount=models.DecimalField(verbose_name=u'有效金额',max_digits=11,decimal_places=2)
    freezeAmount=models.DecimalField(verbose_name=u' 冻结金额金额',max_digits=11,decimal_places=2)
    class Meta:
        verbose_name = u'交易表' 
        verbose_name_plural = '交易表'
        db_table = "charge"
  
'''
订单表
'''  
class Order(models.Model):
    orderId=models.CharField(verbose_name=u'订单号',max_length=11)
    amount=models.DecimalField(verbose_name=u'交易金额',max_digits=11,decimal_places=2)
    currency=models.CharField(verbose_name=u'货币类型',max_length=11)
    type=models.CharField(verbose_name=u'交易类型',max_length=5)
    status=models.CharField(verbose_name=u'交易状态',max_length=11,choices=(('initiated',u'未支付'),('completed',u'成功'),('failed',u'失败'),))
    createTime=models.DateTimeField(verbose_name=u'创建时间')
    updateTime=models.DateTimeField(verbose_name=u'更新时间',null=True,blank=True)
    data=models.CharField(verbose_name=u'说明',max_length=255,null=True,blank=True)
    class Meta:
        verbose_name = u'订单表' 
        verbose_name_plural = '订单表'
        db_table = "order"

'''
拼爱币兑换关系表
'''
class ChargeExchangeRelate():
    type=models.CharField(verbose_name=u'操作类型',max_length=10)
    amount=models.IntegerField(verbose_name=u'获得积分数量')
    instruction=models.CharField(verbose_name=u'说明',max_length=255,)
    class Meta:
        verbose_name = u'拼爱币兑换关系表' 
        verbose_name_plural = u'拼爱币兑换关系表'
        db_table = "charge_exchange_relate"