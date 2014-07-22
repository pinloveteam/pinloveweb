# -*- coding: utf-8 -*-
'''
Created on Sep 1, 2013

@author: jin
'''
from pinloveweb import settings
CONTENT=u'%s为你购买了分数，请查看<button onclick="show_detail_info(this);" value="%s">查看</bubutton>'
BUY_SCORE_FOR_OTHER_MESSAGE_TEMPLATE=getattr(settings, 'BUY_SCORE_FOR_OTHER_MESSAGE_TEMPLATE', CONTENT)
#网站的外貌打分默认投票数
DEFAULT_WEB_VOTE_NUM=100