#-*- coding: utf-8 -*-
'''
Created on 2014年6月27日

@author: jin
'''
from apps.alipay_app.alipay_setting import config
import hashlib
'''
     * 签名字符串
     * @param text 需要签名的字符串
     * @param key 密钥
     * @return 签名结果
'''
def sign_MD5(text,key):
    content='%s%s'%(text,key)
    MD5=hashlib.md5(content)
    return MD5.hexdigest()

def verify_MD5(text,sign,key):
    content='%s%s'%(text,key)
    if sign==text:
        return True
    else:
        return False
    
'''
签名字符串

'''   
def sign(text,key,type='MD5'):
    if type=='MD5':
        return sign_MD5(text,key)