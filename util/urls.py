# -*- coding: utf-8 -*-
'''
Created on Dec 30, 2013

@author: jin
'''
from django.utils.http import is_safe_url
def next_url(request):
    """
    Returns URL to redirect to from the ``next`` param in the request.
    """
    next = request.REQUEST.get("next", "")
    host = request.get_host()
    return next if next and is_safe_url(next, host=host) else None