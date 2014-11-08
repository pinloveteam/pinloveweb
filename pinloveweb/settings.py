# -*- coding: utf-8 -*-
# Django settings for pinlove project.
import os
import sys
PATH=os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
ADMIN_MEDIA_PREFIX = '/admin_media/'


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False



# Additional locations of static files
STATICFILES_DIRS = (
   ('css',os.path.join(PATH,'static/css').replace('\\','/') ),  
    ('js',os.path.join(PATH,'static/js').replace('\\','/') ), 
    ('img',os.path.join(PATH,'static/img').replace('\\','/') ), 
     os.path.join(PATH,'apps/upload_avatar/static').replace('\\','/'), 
     os.path.join(PATH,'apps/user_app/static').replace('\\','/'),
     os.path.join(PATH,'apps/verification_app/static').replace('\\','/'),
     os.path.join(PATH,'apps/pay_app/static').replace('\\','/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'buxmr2-s(7c6)fd_omfcdh_e3w!*oi)yc222=v=5c_0=x79#00'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #登录拦截     
     'middleware.authentication.AuthenticationMiddleware',
     #facebook
#     'apps.third_party_login_app.django_facebook.middleware.FacebookDebugCookieMiddleware',
#     'apps.third_party_login_app.django_facebook.middleware.FacebookDebugTokenMiddleware',
#     'apps.third_party_login_app.django_facebook.middleware.FacebookDebugCanvasMiddleware',
    'apps.third_party_login_app.django_facebook.middleware.FacebookMiddleware',
    #'middleware.timezone.TimezoneMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django.middleware.cache.UpdateCacheMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.cache.FetchFromCacheMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS=(
    "django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
'django.core.context_processors.request',
)

ROOT_URLCONF = 'pinloveweb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pinloveweb.wsgi.application'

TEMPLATE_DIRS = (
     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.="/static/img/logo.png"/></a></d
    # Don't forget to use absolute paths, not relative paths.
)
templates=['templates','apps/user_app/templates','apps/upload_avatar/templates','apps/recommend_app/templates',
               'apps/game_app/templates','apps/verification_app/templates','apps/message_app/templates','apps/friend_dynamic_app/templates',
               'apps/pay_app/templates','apps/user_score_app/templates']
for template in templates:
    TEMPLATE_DIRS += (os.path.join(PATH,template).replace('\\','/'),) 


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.user_app',
    'apps.upload_avatar',
    'apps.search_app',
    'apps.recommend_app',
    'apps.common_app',
    'apps.publish_app',
    'apps.verification_app',
    'apps.message_app',
    'apps.friend_dynamic_app',
    'apps.the_people_nearby',
    'apps.third_party_login_app',
    'apps.pay_app',
    'util',
    #监控memcahe
#     'django_memcached',
#     'social_auth',
#     'grappelli',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
#     'djcelery',   
    'apps.task_app',    
'apps.user_score_app', 
'paypal.standard.ipn',
'apps.alipay_app',
)
 
PAYPAL_RECEIVER_EMAIL = "pinloveteam@gmail.com"
PAYPAL_TEST=False
#test account
# PAYPAL_RECEIVER_EMAIL = "pinloveteam-facilitator@gmail.com"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }
# #logging 日志
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console':{
#             'level':'DEBUG',
#             'class':'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#     }
# }
logger_app=['pinloveweb','apps.friend_dynamic_app','apps.game_app','apps.message_app',
            'apps.pay_app','apps.recommend_app','apps.search_app','the_people_nearby','apps.third_party_login_app','apps.user_app','apps.user_score_app','apps.verification_app','apps.alipay_app']
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(name)s %(asctime)s %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(name)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'django_request':{
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s status_code:%(status_code)d',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'django_db_backends':{
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'log_file':{
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(PATH), 'logs/django.log').replace('\\','/'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216', # 16megabytes(16M)
            'formatter': 'verbose'
        },
        'django_request_logfile':{
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(PATH), 'logs/django_request_logfile.log').replace('\\','/'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216', # 16megabytes(16M)
            'formatter': 'django_request'
        },
        'django_db_backends_logfile':{
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(PATH), 'logs/django_db_backends_logfile.log').replace('\\','/'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216', # 16megabytes(16M)
            'formatter': 'django_db_backends'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console','log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins','django_request_logfile'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['django_db_backends_logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        
        'pinloveweb': {#then you can change the level to control your custom app whether to output the debug infomation
            'handlers': ['log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
#         'customapp.engine': {#then you can change the level to control your custom app whether to output the debug infomation
#             'handlers': ['custom_log_file'],
#             'level': 'WARNING',
#             'propagate': True,
#         },
    },
}
for app in logger_app:
    LOGGING['handlers'][app]={
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(PATH), 'logs/'+app+'.log').replace('\\','/'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216', # 16megabytes(16M)
            'formatter': 'verbose'
        }
    LOGGING['loggers'][app]={#then you can change the level to control your custom app whether to output the debug infomation
            'handlers': [app,'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    
    
# Host for sending e-mail.
EMAIL_HOST = 'smtp.webfaction.com'


# Port for sending e-mail.
EMAIL_PORT = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'pinloveteam'
EMAIL_HOST_PASSWORD = 'redyellowblue123#'
DEFAULT_FROM_EMAIL = 'pinloveteam@pinpinlove.com'
SERVER_EMAIL = 'pinloveteam@pinpinlove.com'
EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = 'email_message/' # change this to a proper location

#set the session paramter session的控制
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE=60*60*12
#缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT':0,
    },
}
# 本地环境
# DATABASES = {
#                                   
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'django',                      # Or path to database file if using sqlite3.
#                                                 # The following settings are not used with sqlite3:
#         'USER': 'root',                         #pinloveteam
#         'PASSWORD': 'jin521436',                       #redyellowblue123#
#         'HOST': '',                             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': '',      
#                                                 # Set to empty string for default.
#     }
# }
# MEDIA_URL = '/media/'
# STATIC_URL = '/static/'
# MEDIA_ROOT = os.path.join(os.path.dirname(PATH),'update').replace('\\','/')
# STATIC_ROOT = os.path.join(PATH,'static').replace('\\','/')
# UPLOAD_AVATAR_UPLOAD_ROOT= os.path.join(os.path.dirname(PATH),'update/user_img').replace('\\','/')
# UPLOAD_AVATAR_AVATAR_ROOT= os.path.join(os.path.dirname(PATH),'update/user_img').replace('\\','/')
# UPLOAD_AVATAR_URL_PREFIX_ORIGINAL='/media/user_img/'
# UPLOAD_AVATAR_URL_PREFIX_CROPPED='/avatar/'
# DOMAIN='pinlove.xicp.net'
# DEBUG = True
# TEMPLATE_DEBUG = DEBUG

#---服务器环境-----
 DEBUG = False
 TEMPLATE_DEBUG = DEBUG
 DATABASES = {
                                       
      'default': {
          'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
          'NAME': 'pinlove_db_1',                      # Or path to database file if using sqlite3.
                                                  # The following settings are not used with sqlite3:
          'USER': 'pinloveteam',
          'PASSWORD': 'redyellowblue123#',
          'HOST': '',                             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
          'PORT': '',                             # Set to empty string for default.
          'OPTIONS':{'init_command':'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci',},
      }
  }
upload 上传地址
 MEDIA_URL = '/media/'
 MEDIA_ROOT =os.path.join(os.path.dirname(PATH),'update').replace('\\','/')
 #静态文件地址
 STATIC_ROOT = os.path.join(PATH,'static').replace('\\','/')
 STATIC_URL = '/static/'
 #头像上传地址
 UPLOAD_AVATAR_UPLOAD_ROOT= os.path.join(os.path.dirname(PATH),'update/user_img').replace('\\','/')
 UPLOAD_AVATAR_AVATAR_ROOT=os.path.join(os.path.dirname(PATH),'update/user_img').replace('\\','/')
 UPLOAD_AVATAR_URL_PREFIX_ORIGINAL='/media/user_img/'
 #grappelli
 UPLOAD_AVATAR_URL_PREFIX_CROPPED='/avatar/'
 ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"
 DOMAIN='pinlove.com'

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
###################for tests##########
# import djcelery
# djcelery.setup_loader()
# 
# ## Celery config ##
# 
# BROKER_URL = "amqp://guest:guest@localhost:5672//"
# 
# 
# CELERY_ALWAYS_EAGER = True
# CELERY_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'apps.task_app.backends.CeleryEmailBackend'
#  
# CELERY_EMAIL_TASK_CONFIG = {
#     'queue' : 'django_email',
#     'delivery_mode' : 1, # non persistent
#     'rate_limit' : '50/m', # 50 emails per minute
# }


'''
facebook 
'''
FACEBOOK_APP_ID = '400350543428768'
FACEBOOK_SECRET_KEY = 'fafdcdabccd34c67311c41489de8dcc2'
# FACEBOOK_APP_ID = '1435511770015401'
# FACEBOOK_SECRET_KEY = '5d31e123edbd191f5f86a86365d02be6'
FACEBOOK_CANVAS_PAGE = 'https://apps.facebook.com/%s/' % FACEBOOK_APP_ID
# Optionally set default permissions to request, e.g: ['email', 'user_about_me']
# FACEBOOK_SCOPE = ['publish_stream','user_location']
FACEBOOK_SCOPE = ['user_location','user_birthday','user_photos','user_education_history','user_work_history','friends_online_presence']


# And for local debugging, use one of the debug middlewares and set:
FACEBOOK_DEBUG_TOKEN = 'CAACEdEose0cBALArzVDGYCOfNl9qJs3W9dTZCpescXb5eRmAn4SIZBRsliYjPZA2ny0TZBFIpkqwsJ2v0UbU2B3xpJmrS39IqNwmislZCSJgZCA6ZBsbRXZCxrFHN66a7rU8wG2aJiRhVXr9frWuZAbWbh88dgC72YLNCerWYu0RKEZBlawvqbpR6g0sM9D6kkaVZCly7uy4QFY5wZDZD'
FACEBOOK_DEBUG_UID = '100007203789389'
FACEBOOK_DEBUG_COOKIE ='AzIUY1rpSMWthv3CUdBFebFV8Z_clRlDazXq1sHPzjQ.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUJ2WnFSSXp5YnEzX0JCZngyYUdyLXB0S0VZZk5xQ2dNOHg2MXd3QVF3U3dvMkdJRUlwSi1MLW13bEtHbHhzbkd6Y2JveV8teFdhb1NHZEhwUzIxTmo0azU2WHJNSmdnSmZhdHI5VVhWRlRuZUxWelV5eURYYnNIV2dzM0h5QjVkTnI2ajI2ckhxbDQxV3lmMFIyRl9INkZQTEdNdXBpS3VKMm14TzhGUXBlQ0tvNGRlQzBjSlN3Slo1RmFhMDZsNmhCZ1A1OEMxQ2NLQlJEUktzVWJ4aFNCcVdqN0xjMkhZZUM3WHRQZGF4WWhUU2Nkby11cThWVzlQdkszOUdWMjlnc1daMnFNbEFkWEQ3Y0ROQjk2S1lEZ2tWbkk4S00wSW9QMnNyU1NsNXU4ODZONGR0LUVYS05NOER6dTdiQng3QXlPeU9nVWZLTWpmTk5Id1l0VW43RSIsImlzc3VlZF9hdCI6MTM5MjYxODc2NCwidXNlcl9pZCI6IjEwMDAwNzIwMzc4OTM4OSJ9'
FACEBOOK_DEBUG_SIGNEDREQ ='6sZoh3-0-nHQejXO-gAIrtMel76FWQR7OupEkqAS0TU.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImV4cGlyZXMiOjEzOTQwMTM2MDAsImlzc3VlZF9hdCI6MTM5NDAwNjY0NCwib2F1dGhfdG9rZW4iOiJDQUFGc0hkWkN0UEtBQkFETlJaQUpqMHRmbVdsMTJiQ2ppN0tkczhaQlpBSUVjYzM4NEc5cDlmRDNPZVZDMVpCbFY3cXJZU2llNDkyS3pSZzVjWkJJQjZkRlVzcHNCVUxzMjJqYnVQNnEyMHRtOUV3Y2tNR1NLZmdaQjRhUllFRzBvWkNYVWd0VldlTjBEYzBKZzVhb0hZNjdPWkJJZk5OdERwR3lzUWZxNEhSQXZscTlqaXpmdnBpVjUxY3ZqQkhuaXhNdHQ3a0ZXSWtrZHl3WkRaRCIsInVzZXIiOnsiY291bnRyeSI6InVzIiwibG9jYWxlIjoiZW5fVVMiLCJhZ2UiOnsibWluIjoxMywibWF4IjoxN319LCJ1c2VyX2lkIjoiMTAwMDA3MjQ3NDcwMjg5In0'
# FACEBOOK_DEBUG_SIGNEDREQ ='RoHqy693wl3t917auOIyLYavI8ZDUP5L3RKj4T_01IU.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImV4cGlyZXMiOjEzOTUzNzQ0MDAsImlzc3VlZF9hdCI6MTM5NTM2OTQ2MCwib2F1dGhfdG9rZW4iOiJDQUFGc0hkWkN0UEtBQkFOcEZ0QWdMVzJqWkFwejliNG93S3BYYUVOd2F0aWlGWkFRZzlpU1FzbGxUMmZrb21oQkYzVzhTdkpnWkMwa2tZdllMNVU4Q1JDNG5INDg4ek9WenJ6NEdXeThaQnNnVjhZWkNoUTU4SGNzMnZMNnc4S2FXd0RFZFpBdFpCa3ZvbVpCQnptR0g1WkJWMndMUXZHMlc2ZUVxV1RIbnhTVWRuZXRPR1ZZZW5tekxLOUI3cUM5cEtQakNWRFpCNkFVeWdRVmdaRFpEIiwidXNlciI6eyJjb3VudHJ5IjoianAiLCJsb2NhbGUiOiJlbl9VUyIsImFnZSI6eyJtaW4iOjEzLCJtYXgiOjE3fX0sInVzZXJfaWQiOiIxMDAwMDcyNDc0NzAyODkifQ'
#admin id
ADMIN_ID=1
if __name__=='__main__':
    print os.path.join(os.path.dirname(PATH),'update').replace('\\','/')