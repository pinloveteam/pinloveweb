from django.contrib.auth.models import User
from apps.game_app import jigswgl
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.user_app.models import UserProfile

@csrf_exempt
def jigsaw(request):
    selected=request.POST.get("selected",'') 
    username = request.user.username
    gender = UserProfile.objects.get(user=request.user).gender
    selected_set = [int(i) for i in selected.split("-") if i]
    cha1 = jigswgl.UNIVERSAL_SET - set(selected_set)
    cha2 = set(selected_set) - jigswgl.UNIVERSAL_SET
    
    if cha1 != jigswgl.UNIVERSAL_SET and cha1 != set([]) and cha2 == set([]) and username not in jigswgl.JIGSWABLE:
        if gender == 'M':
            otherone = jigswgl.JIGSW_GIRLS.get(str(cha1))
            jigswgl.JIGSW_BOYS[str(set(selected_set))] = username
        else :
            jigswgl.JIGSW_GIRLS[str(set(selected_set))] = username
            otherone = jigswgl.JIGSW_BOYS.get(str(cha1))
                
        jigswgl.JIGSWABLE.add(username)
        obj = [{'message':'null'}]
        if otherone != None:
            otheruser = UserProfile.objects.get(user=User.objects.get(username=otherone))
            print otheruser.height
            print otheruser.age
            print otheruser.avatar_name
            obj = [{'message':otherone,'height':otheruser.height,'age':otheruser.age,'avatar_name':otheruser.avatar_name}]
        e = simplejson.dumps(obj) 
        return HttpResponse(e, mimetype='application/javascript')   
    else:
        obj = [{'message':'error'}]
        e = simplejson.dumps(obj) 
        return HttpResponse(e, mimetype='application/javascript') 

def pintu(request):
    return render(request, 'pintu.html')
