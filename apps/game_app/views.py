#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.game_app.models import Yuanfenjigsaw, get_count


@csrf_exempt
def jigsaw(request):
    match_result = Yuanfenjigsaw(request).get_match_result()
    json=simplejson.dumps(match_result)
    return HttpResponse(json, mimetype='application/javascript')

def pintu(request):
    from apps.third_party_login_app.models import FacebookUser
    username=FacebookUser.objects.get(uid=request.facebook.uid).username
    count = get_count(username)
    return render(request, 'pintu.html',{'count':count})


