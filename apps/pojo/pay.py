# -*- coding: utf-8 -*-
'''
Created on 2015年1月17日

@author: jin
'''
#========================
#价格表
#attribute： 
#       price 拼爱币价格
#       presentation  赠送 
#=======================
class PriceRelate(object):
    def __init__(self,*args,**kwargs):
        pinLovePrice=kwargs.pop('pinLovePrice',0)
        pinLovePresentation=kwargs.pop('pinLovePresentation',0)
        currencyPrice=kwargs.pop('currencyPrice',0)
    def discount(self,num):
        #商品打折
        self.currencyPrice=self.currencyPrice*num