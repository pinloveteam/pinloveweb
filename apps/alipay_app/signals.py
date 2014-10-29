#-*- coding: utf-8 -*-
'''
Created on 2014年7月4日

@author: jin
'''
from django.dispatch import Signal
from apps.pay_app.alipay import update_order_charge_by_alipay

# Sent when a payment is successfully processed.
alipay_dpn_successful = Signal()

alipay_dpn_flagged = Signal()


alipay_dpn_successful.connect(update_order_charge_by_alipay) 