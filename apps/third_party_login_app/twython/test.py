# -*- coding: utf-8 -*-
'''
Created on Dec 17, 2013

@author: jin
'''
from apps.third_party_login_app.setting import TwitterConsumerKey,\
    TwitterConsumerSecret
from apps.third_party_login_app.twython.api import Twython
access_token_key='2249878794-QGk7iGnMgFQZAttHYV1HJjbkjTJTkFtOR6PqVsn'
# access_token_secret='9AsQvWkKEYai7u65TMH2Fcnqcvp6tdV04XPGUNFN5C3Te'
# api = Twython(TwitterConsumerKey, TwitterConsumerSecret, access_token_key, access_token_secret)
twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret)
auth = twitter.get_authentication_tokens(callback_url='')
print auth
# OAUTH_TOKEN = auth['oauth_token']
# OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
# twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret,'2249878794-QGk7iGnMgFQZAttHYV1HJjbkjTJTkFtOR6PqVsn','9AsQvWkKEYai7u65TMH2Fcnqcvp6tdV04XPGUNFN5C3Te')
# access=twitter.get_authorized_tokens('CFfgwUDvZny1QIMPnMTrXDsn5bAllbQbauWIMkZP0M')
# twitter = Twython(TwitterConsumerKey, TwitterConsumerSecret,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
# auth = twitter.get_authentication_tokens(callback_url='http://snailjin.eicp.net/third_party_login/twitter_login_url/')
# print auth['oauth_token']
# i=api.verify_credentials()
# i=twitter.verify_credentials()
# print i