import os, sys


#Calculate the path based on the location of the WSGI script.

sys.path.append(r'/home/pinloveteam/webapps/pinlove/pinloveweb')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pinloveweb.settings'

os.environ['PYTHON_EGG_CACHE'] = '/tmp'


import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

