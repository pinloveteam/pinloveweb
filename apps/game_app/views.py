#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.game_app.models import Yuanfenjigsaw, get_count

@csrf_exempt
def jigsaw(request):
    match_result = Yuanfenjigsaw(request).get_match_result()
    return HttpResponse(simplejson.dumps(match_result), mimetype='application/javascript')

def pintu(request):
    count = get_count(request)
    return render(request, 'pintu.html',{'count':count})
