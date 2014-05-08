# -*- coding: utf-8 -*-
'''
Created on 2014年5月2日

@author: jin
'''
from pinloveweb import settings
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
import logging
from apps.pay_app.models import Order, Charge
import uuid
import datetime
from django.db import transaction

def asks_for_money(request):

    # What you want the button to do.
    orderId=('%s%s%s' %('DD',request.user.id,uuid.uuid4()))[0:10]
    amount=0.01
    from apps.pay_app.pay_setting import PAYPAL
    paypal_dict = {
        "business": PAYPAL['PAYPAL_RECEIVER_EMAIL'],
        "amount":amount,
        "item_name": "pinlove",
        "invoice": orderId,
        "notify_url": PAYPAL['PAYPAL_URL']+"/pay/paypal/",
        "return_url": PAYPAL['PAYPAL_URL']+"/pay/paypal_success/",
        "cancel_return": PAYPAL['PAYPAL_URL']+"/pay/paypal_cancel/",

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    Order(user_id=request.user.id,orderId=orderId,amount=amount,status='initiated',type='2',data=u"拼爱币充值").save()
    return context

from paypal.standard.ipn.signals import payment_was_successful
@transaction.commit_on_success  
def show_me_the_money(sender,**kwargs):
    ipn_obj = sender
    # You need to check 'payment_status' of the IPN
    if ipn_obj.payment_status == "Completed":
        if Order.objects.filter(orderId=ipn_obj.invoice).exists():
            logging.error('orderId exists')
            order=Order.objects.get(orderId=ipn_obj.invoice)
            order.currency=ipn_obj.mc_currency
            order.status="completed"
            order.updateTime=datetime.datetime.today()
            order.save()
            charge=Charge.objects.get(user_id=order.user_id)
            charge.vailAmount+=order.amount
            charge.save()
            logging.error('保存完毕')
    
payment_was_successful.connect(show_me_the_money) 