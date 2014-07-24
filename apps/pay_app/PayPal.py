# -*- coding: utf-8 -*-
'''
Created on 2014年5月2日

@author: jin
'''
from paypal.standard.forms import PayPalPaymentsForm
import logging
from apps.pay_app.models import Order, Charge, ChargeDetail
import datetime
from django.db import transaction
logger=logging.getLogger(__name__)
#===============================
#生成paypal订单
#===============================
def asks_for_money(userId,amount=0,price=0.00,currency='USB',data=''):
  try:
    # What you want the button to do.
    order=Order(user_id=userId,currency=currency,amount=amount,price=price,status='initiated',type='2',channel='2',pattern='1')
    order.data=order.get_pattern_display()
    order.get_order_id(userId)
    from pinloveweb.settings import PAYPAL_RECEIVER_EMAIL,DOMAIN
    paypal_dict = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "amount":price,
        "item_name": "pinlove",
        "invoice": order.orderId,
        "notify_url": '%s%s%s' %('http://',DOMAIN,"/pay/paypal/"),
        "return": '%s%s%s' %('http://',DOMAIN,"/pay/member/"),
        "cancel_return": '%s%s%s' %('http://',DOMAIN,"/pay/paypal_cancel/"),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    order.save()
    return context
  except Exception as e:
      logger.exception('%s%s' %('生成paypal订单出错，出错原因：',e)) 

from paypal.standard.ipn.signals import payment_was_successful
@transaction.commit_on_success  
def show_me_the_money(sender,**kwargs):
  try:
    ipn_obj = sender
    # You need to check 'payment_status' of the IPN
    if ipn_obj.payment_status == "Completed":
        logger.error('============ipn_obj  Completed')
        if Order.objects.filter(orderId=ipn_obj.invoice).exists():
            order=Order.objects.get(orderId=ipn_obj.invoice)
            logger.error('============Order  exists')
            if ipn_obj.mc_gross==order.price:
                 logger.error('============price  222')
                 order.status="completed"
                 order.updateTime=datetime.datetime.today()
                 order.save()
                 #板寸交易详细
                 ChargeDetail(user_id=order.user_id,amount=order.amount,time=order.updateTime,type='1001',orderId=order.orderId,
                              data='%s%s%s'%('充值',order.amount,'拼爱币')).save()
                 charge=Charge.objects.get(user_id=order.user_id)
                 charge.validAmount+=order.amount
                 charge.save()
            else:
                logger.error('============price  1111')
               order.status="failed"
               order.updateTime=datetime.datetime.today()
               order.failReason=u'金额错误，金额不相等'
               order.save()
  except Exception ,e:
      logger.exception('更新paypal订单出错！')
      order.status="failed"
      order.updateTime=datetime.datetime.today()
      order.failReason=e.message
      order.save()
        
    
payment_was_successful.connect(show_me_the_money) 

