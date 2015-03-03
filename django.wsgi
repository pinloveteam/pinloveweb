import os
import sys
import django.core.handlers.wsgi

sys.path.append(r'E:/eclipse_64/code/pinloveweb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pinloveweb.settings'
application = django.core.handlers.wsgi.WSGIHandler()