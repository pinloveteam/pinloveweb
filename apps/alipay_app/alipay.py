#-*- coding: utf-8 -*-
'''
Created on 2014年6月27日

@author: jin
'''
from apps.pay_app.models import Order
from apps.alipay_app.alipay_setting import config
from apps.alipay_app.forms import AliPayDirectPayForm
from apps.alipay_app.helper import get_form_data, buildRequestMysign
import logging
from django.utils import simplejson
logger=logging.getLogger(__name__)            
    

    
'''
生成aplipay订单
'''
def build_aplipay_order(userId,amount=1,price=0.00,currency='RMB',data=''):
  try:
    # What you want the button to do.
    order=Order(user_id=userId,currency=currency,amount=amount,price=price,status='initiated',type='2',channel='2',pattern='1')
    order.data=order.get_pattern_display()
    order.get_order_id(userId)
    from pinloveweb.settings import PAYPAL_RECEIVER_EMAIL,DOMAIN
    aplipay_dict = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "price":price,
        "subject": config.subject,
        "out_trade_no": order.orderId,
        'quantity':1,
        'notify_url':config.ALIPAY_NOTIFY_URL,
        'return_url':config.ALIPAY_RETURN_URL,
        'body':'%s%s%s'%('购买拼爱币',amount,'个')
        
    }
    form = AliPayDirectPayForm(initial=aplipay_dict)
    data = get_form_data(form)
    sign=buildRequestMysign(data)
    form['sign'].field.sign,form.initial['sign']=sign,sign
    context = {"form": form}
    order.save()
    return context
  except Exception as e:
      print '%s%s' %('生成alipay订单出错，出错原因：',e)



# def update_order_by_aplipay(AliPay):
#     if 