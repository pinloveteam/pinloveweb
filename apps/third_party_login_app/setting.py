# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2013

@author: jin

'''
WEB_ROOT='http://snailjin.eicp.net'
# WEB_ROOT='http://pinlove.com/'

DEFAULT_PASSWORD='PIN_LOVE_10086'
#sign in with QQ
QQAPPID='100571298'
QQAPPKEY='9e036c3878a706fcb844064fd029bf5a'
QQ_CALLBACK_URL=WEB_ROOT+'/third_party_login/qq_login/'

#sign in with sina
SinaAppKey='2523894606'
SinaAppSercet='a71027f332b9252e91c2a0faab61d867'
SINA_CALLBACK_URL =WEB_ROOT+'/third_party_login/sina_login/' # callback url

#sign in whth facebook 
FaceBookAppID='1412943645609984'
FaceBookAppSecret='4613e006bced32e5e124f65f5bc997fe'
FACEBOOK_CALLBACK_URL = WEB_ROOT+'/third_party_login/facebook_login/'

#sign in whth twitter
TwitterConsumerKey='nypTu4l4D1sQVef8LgWjQ'
TwitterConsumerSecret='OFAdY6pCfAHpmCjoOUdvpCLYao3rxG1QB1DpEtiblE'
TWITTER_CALLBACK_URL= WEB_ROOT+'/third_party_login/twitter_login/'

#生产环境的使用，如测试环境请注释
# FaceBookAppID='400350543428768'
# FaceBookAppSecret='fafdcdabccd34c67311c41489de8dcc2'