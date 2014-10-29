# -*- coding: utf-8 -*-
'''
Created on 2014年7月4日

@author: jin
'''
from apps.pay_app.models import Order, ChargeDetail, Charge
from django.utils import simplejson
import logging
import datetime
from django.db import transaction
logger=logging.getLogger(__name__)
@transaction.commit_on_success
def update_order_charge_by_alipay(sender,**kwargs):
  try:
#     logger.error('alipay============price  222')
    obj=sender
    flag=True
    if not  Order.objects.filter(orderId=obj.out_trade_no).exists():
        raise Exception('%s%s'%('支付宝订单和网站部对应（网站订单不存在）!支付宝参数:',simplejson.dumps(obj.__dict__)))
    if obj.trade_status=='TRADE_SUCCESS':
         order=Order.objects.get(orderId=obj.out_trade_no)
         if float(obj.total_fee)==float(order.price):
             order.status="completed"
         else:
            order.status="failed"
            order.failReason=u'金额错误，金额不相等'
    else:
        order.status="failed"
        order.failReason=u'支付宝失败'
    order.updateTime=datetime.datetime.today()
    order.save()
    #交易详细
    if order.status=="completed":
        ChargeDetail(user_id=order.user_id,amount=order.amount,time=order.updateTime,type='1001',orderId=order.orderId,
                              data='%s%s%s'%('充值',order.amount,'拼爱币')).save()
        charge=Charge.objects.get(user_id=order.user_id)
        charge.validAmount+=order.amount
        charge.save()
  except Exception as e:
      logger.exception(e.message)