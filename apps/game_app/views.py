#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.game_app.models import Yuanfenjigsaw, get_count

import datetime
from django.core.cache import cache

cache.set('ALL_PIECE',set([0,1,2,3,4,5,6,7,8,9]))
cache.set('GAME_TIMES',10)
cache.set('NO_MATCHING_USER',"0")
cache.set('DATA_UNAVAILABLE',"1")
cache.set('GAME_TIMES_REACH_THE_LIMIT',"2")
cache.set('MATCH_SUCCESS',"3")
cache.set('TODAY',datetime.date.today())
cache.set('GIRLS',{})
cache.set('BOYS',{})
cache.set('USER_GAME_COUNT',{})
@csrf_exempt
def jigsaw(request):
    match_result = Yuanfenjigsaw(request).get_match_result()
    json=simplejson.dumps(match_result)
    return HttpResponse(json, mimetype='application/javascript')

def pintu(request):
    count = get_count(request)
    return render(request, 'pintu.html',{'count':count})
