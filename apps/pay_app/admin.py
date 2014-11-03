# -*- coding: utf-8 -*-
'''
Created on 2014年10月31日

@author: jin
'''
from django.contrib import admin
from paypal.standard.ipn.models import PayPalIPN
from apps.pay_app.models import Order, ChargeExchangeRelate, Charge,\
    ChargeDetail
"""
paypal支付表
"""
# class PayPalIPNAdmin(admin.ModelAdmin):
#     date_hierarchy = 'payment_date'
#     list_display = [
#         "invoice","payer_status","payer_email", "first_name", "last_name","mc_gross","created_at", "flag", "flag_info", 
#     ]
#     search_fields = ["invoice", "payer_email"]


# admin.site.register(PayPalIPN, PayPalIPNAdmin)
"""
订单表
"""
class OrderAdmin(admin.ModelAdmin):
    payment_date="payment_date"
    list_display = [
        "orderId","status","user","price", "amount", "currency","channel","type", "pattern", "createTime",
        "updateTime","data","failReason"
    ]
    list_filter=('channel','type','status',)
    search_fields = ["orderId", "user"]
    
admin.site.register(Order, OrderAdmin)
"""
拼爱币兑换关系表
"""
class ChargeExchangeRelateAdmin(admin.ModelAdmin):
    list_display = [
        "PLPrice","PLPresentation","currencyPrice","discount", "currencyType", "operateType","instruction",
    ]
    list_filter=('currencyType','operateType',)
admin.site.register(ChargeExchangeRelate, ChargeExchangeRelateAdmin)

"""
拼爱币
"""
class ChargeAdmin(admin.ModelAdmin):
    list_display = [
        "user","validAmount", "freezeAmount",
    ]
    search_fields = ["user",]
    
admin.site.register(Charge, ChargeAdmin)

"""
拼爱币
"""
class ChargeDetailAdmin(admin.ModelAdmin):
    payment_date="payment_date"
    list_display = [
        "user", "amount", "data","time","type", "orderId",
    ]
    list_filter=('orderId','user',)
    search_fields = ["type",]
    
admin.site.register(ChargeDetail, ChargeDetailAdmin)