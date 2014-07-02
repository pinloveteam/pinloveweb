#-*- coding: utf-8 -*-
'''
Created on 2014年6月27日

@author: jin
'''
from django.conf import settings
'''
接口
'''
SERVICE=['create_direct_pay_by_user',]
#ip白名单
ALIPAY_NOTIFY_IP = getattr(settings, 'ALIPAY_NOTIFY_IP',('121.0.26.0/23', '110.75.128.0/19'))
#支付类型
PAYMENT_TYPE = (
        '1', #商品购买
        '2', #服务购买
        '3', #网络拍卖
        '4', #捐赠
        '5', #邮费补偿
        '6', #奖金
        '7', #基金购买
        '8', #机票购买
        )

ALIPAY_DATE_FORMAT= ('%Y-%m-%d %H:%M:%S',)
class config:
    ALIPAY_KEY = 'q3bgn0y4b6ssm26x5mgm13usm5f9b2jy'

    ALIPAY_INPUT_CHARSET = 'utf-8'

    # 合作身份者ID，以2088开头的16位纯数字
    ALIPAY_PARTNER = 2088411296074165
    #卖家支付账号
    ALIPAY_SELLER_ID = getattr(settings, 'ALIPAY_SELLER_ID', 2088411296074165)

    # 签约支付宝账号或卖家支付宝帐户
    ALIPAY_SELLER_EMAIL = 'liuye65426@sina.cn'

    ALIPAY_SIGN_TYPE = 'MD5'

    # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_RETURN_URL='%s%s%s' %('http://',settings.DOMAIN,"/alipay/paid/")

    # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_NOTIFY_URL='%s%s%s' %('http://',settings.DOMAIN,"/alipay/")

    ALIPAY_SHOW_URL=''

    # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
    ALIPAY_TRANSPORT='https'
    
    #网关
    ALIPAY_GATEWAY = "https://mapi.alipay.com/gateway.do"
    
    #商品名称
    subject='拼爱币'
 