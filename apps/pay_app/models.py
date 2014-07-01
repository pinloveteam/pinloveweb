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
    user=models.ForeignKey(User,verbose_name='用户id')
    validAmount=models.IntegerField(verbose_name=u'有效金额',default=0)
    freezeAmount=models.IntegerField(verbose_name=u' 冻结金额金额',default=0)
    class Meta:
        verbose_name = u'交易表' 
        verbose_name_plural = '交易表'
        db_table = "charge"
  
'''
交易表
'''       
class ChargeDetail(models.Model):
    user=models.ForeignKey(User,verbose_name='用户id')
    amount=models.IntegerField(verbose_name=u'交易数量',)
    data=models.CharField(verbose_name=u'说明',max_length=255)
    time=models.DateTimeField(verbose_name=u'时间',)
    #ChargeExchangeRelate表 operateType
    type=models.CharField(verbose_name=u'操作类型',max_length=11)
    #Order 表主键
    orderId=models.CharField(verbose_name=u'订单号',max_length=27,null=True,blank=True)
    class Meta:
        verbose_name = u'交易明细表' 
        verbose_name_plural = '交易明细表'
        db_table = "charge_detail"
'''
订单表
'''  
class Order(models.Model):
    user=models.ForeignKey(User,verbose_name='用户id')
    orderId=models.CharField(verbose_name=u'订单号',max_length=27)
    amount=models.IntegerField(verbose_name=u'交易拼爱币数量')
    price=models.DecimalField(verbose_name=u'交易金额',max_digits=11,decimal_places=2)
    currency=models.CharField(verbose_name=u'货币类型',max_length=11)
    channel=models.CharField(verbose_name=u'交易渠道',max_length=2,choices=(('1',u'支付宝'),('2',u'paypal')))
    type=models.CharField(verbose_name=u'交易类型',max_length=2,choices=(('1',u'消耗'),('2',u'获得')),)
    pattern=models.CharField(verbose_name=u'交易方式',max_length=4,choices=(('1',u'拼爱币充值'),('2',u'拼爱币赎回'),('3',u'拼爱币消费')),)
    status=models.CharField(verbose_name=u'交易状态',max_length=11,choices=(('initiated',u'未支付'),('completed',u'成功'),('failed',u'失败'),('cancel',u'关闭'),('dispute',u'纠纷')))
    createTime=models.DateTimeField(verbose_name=u'创建时间')
    updateTime=models.DateTimeField(verbose_name=u'更新时间',null=True,blank=True)
    data=models.CharField(verbose_name=u'说明',max_length=255,null=True,blank=True)
    failReason=models.CharField(verbose_name=u'失败说明',max_length=255,null=True,blank=True)
    #==========================
    #获得订单id
    #==========================
    def get_order_id(self,userId):
        import uuid
        self.orderId=('%s%s%s' %('DD',userId,uuid.uuid4()))[0:20]
    def save(self,*args,**kwargs):
         import datetime
         self.createTime=datetime.datetime.today()
         super(Order, self).save(*args, **kwargs)
    class Meta:
        verbose_name = u'订单表' 
        verbose_name_plural = '订单表'
        db_table = "order"
    #================
    #获得状态
    #================  
    def get_status(self):
         #如果是赎回
         if self.pattern=='2' and self.status=='initiated':
             return '正在等待审核'
         else:
             return self.get_status_display()

'''
拼爱币兑换关系表
'''
class ChargeExchangeRelate(models.Model):
    PLPrice=models.IntegerField(verbose_name=u'拼爱币价格',default=0)
    PLPresentation=models.IntegerField(verbose_name=u'赠送拼爱币个数',default=0)
    currencyPrice=models.DecimalField(verbose_name=u'货币价格',max_digits=11,decimal_places=2,default=0.00,null=True,blank=True)
    discount=models.DecimalField(verbose_name=u'折扣',max_digits=11,decimal_places=2,default=1.00,null=True,blank=True)
    CURRENCY_TYPE_CHOICE=((1,'USB'),(2,'RMB'))
    currencyType=models.SmallIntegerField(verbose_name=u'货币类型',choices=CURRENCY_TYPE_CHOICE,null=True,blank=True)
    OPERATE_TYPE_CHIOCE=(('1001',u'购买拼爱币'),('1002',u'查看别人对你的打分'),)
    operateType=models.CharField(verbose_name=u'操作类型',choices=CURRENCY_TYPE_CHOICE,max_length=11)
    instruction=models.CharField(verbose_name=u'说明',max_length=255,null=True,blank=True)
    def get_amount(self):
        return int(self.PLPrice+self.PLPresentation)
    def get_price(self):
        return self.currencyPrice*self.discount
    class Meta:
        verbose_name = u'拼爱币兑换关系表' 
        verbose_name_plural = u'拼爱币兑换关系表'
        db_table = "charge_exchange_relate"