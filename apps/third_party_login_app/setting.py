# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2013

@author: jin

'''
#生产环境的使用
from pinloveweb import settings
if settings.DEBUG:
    WEB_ROOT='http://pinlove.xicp.net'
    
    DEFAULT_PASSWORD='PIN_LOVE_10086'
    #sign in with QQ
    QQAPPID='100571298'
    QQAPPKEY='9e036c3878a706fcb844064fd029bf5a'
    QQ_CALLBACK_URL=WEB_ROOT+'/third_party_login/qq_login/'
    QQ_MOBILE_CALLBACK_URL=WEB_ROOT+'/mobile/qq_login/'
    
    #sign in with sina
    SinaAppKey='2523894606'
    SinaAppSercet='a71027f332b9252e91c2a0faab61d867'
    SINA_CALLBACK_URL =WEB_ROOT+'/third_party_login/sina_login/' # callback url
    SINA_MOBILE_CALLBACK_URL =WEB_ROOT+'/mobile/sina_login/'
    
    #sign in whth facebook 
    FaceBookAppID='1412943645609984'
    FaceBookAppSecret='4613e006bced32e5e124f65f5bc997fe'
    FACEBOOK_CALLBACK_URL = WEB_ROOT+'/third_party_login/facebook_login/'
    FACEBOOK_MOBILE_CALLBACK_URL = WEB_ROOT+'/mobile/facebook_login/'
    
    #sign in whth twitter
    TwitterConsumerKey='nypTu4l4D1sQVef8LgWjQ'
    TwitterConsumerSecret='OFAdY6pCfAHpmCjoOUdvpCLYao3rxG1QB1DpEtiblE'
    TWITTER_CALLBACK_URL= WEB_ROOT+'/third_party_login/twitter_login/'
    
    #sign in with weixin 平台
    WeiXinAppID=u'wxc3133ce01a166239'
    WeiXinAppSecret='9cd6f602e0c5803b0a439a45b28243b2'
    WEIXIN_CALLBACK_URL =WEB_ROOT+'/third_party_login/weixin_login/'
    WEIXIN_MOBILE_CALLBACK_URL =WEB_ROOT+'/mobile/weixin_login/'
 
    #sign in with weixin 公众号
    PublicWeiXinAppID=u'wxdbf6f94c9d5f7cd1'
    PublicWeiXinAppSecret='142757a23a30830e8f602fe82e5e4874'
#     PublicWeiXinAppID=u'wx89b973cc86752aa7'
#     PublicWeiXinAppSecret='024deb12832ef83c19f9442b2eedc3db'
    WEIXIN_CHECK_AUTHORIZATION_URL =WEB_ROOT+'/third_party_login/weixin_check_authorization/'

else:
    
    WEB_ROOT='http://pinlove.com'
    DEFAULT_PASSWORD='PIN_LOVE_10086'
   
    FaceBookAppID='400350543428768'
    FaceBookAppSecret='fafdcdabccd34c67311c41489de8dcc2'
    FACEBOOK_CALLBACK_URL = WEB_ROOT+'/third_party_login/facebook_login/'
    FACEBOOK_MOBILE_CALLBACK_URL = WEB_ROOT+'/mobile/facebook_login/'
   
    #sign in whth twitter
    TwitterConsumerKey='nypTu4l4D1sQVef8LgWjQ'
    TwitterConsumerSecret='OFAdY6pCfAHpmCjoOUdvpCLYao3rxG1QB1DpEtiblE'
    TWITTER_CALLBACK_URL= WEB_ROOT+'/third_party_login/twitter_login/'
   
    #sign in with QQ
    QQAPPID='100579249'
    QQAPPKEY='d8c6c988791321284df188e4c5e9cad3'
    QQ_CALLBACK_URL=WEB_ROOT+'/third_party_login/qq_login/'
    QQ_MOBILE_CALLBACK_URL=WEB_ROOT+'/mobile/qq_login/'
   
    #sign in with sina
    SinaAppKey='112291859'
    SinaAppSercet='a951c7dac0d23e09ed42e6a6377c8723'
    SINA_CALLBACK_URL =WEB_ROOT+'/third_party_login/sina_login/' # callback url
    SINA_MOBILE_CALLBACK_URL =WEB_ROOT+'/mobile/sina_login/'

    #sign in with weixin 开发平台
    WeiXinAppID=u'wxc3133ce01a166239'
    WeiXinAppSecret='9cd6f602e0c5803b0a439a45b28243b2'
    WEIXIN_CALLBACK_URL =WEB_ROOT+'/third_party_login/weixin_login/'
    WEIXIN_MOBILE_CALLBACK_URL =WEB_ROOT+'/mobile/weixin_login/'

    #sign in with weixin 公众号
    PublicWeiXinAppID=u'wx89b973cc86752aa7'
    PublicWeiXinAppSecret='024deb12832ef83c19f9442b2eedc3db'
    WEIXIN_CHECK_AUTHORIZATION_URL =WEB_ROOT+'/third_party_login/weixin_check_authorization/'