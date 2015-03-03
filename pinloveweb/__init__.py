# -*- coding: utf-8 -*-
# from __future__ import absolute_import
# 
# from celery import app
from util.cache import init_cache
from apps.user_app.method import get_staff_list
init_cache()
#初始化职员名单
STAFF_MEMBERS=get_staff_list()