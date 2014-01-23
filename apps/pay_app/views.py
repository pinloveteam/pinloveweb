# -*- coding: utf-8 -*-
'''
Created on Sep 8, 2013

@author: jin
'''
from django.shortcuts import render
def get_icon(request):
    return render(request,'icon.html')