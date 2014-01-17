# -*- coding: utf-8 -*-
# Django settings for pinlove project.
import os
PATH=os.path.dirname(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

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
USE_TZ = True



# Additional locations of static files
STATICFILES_DIRS = (
   ('css',os.path.join(PATH,'static/css').replace('\\','/') ),  
    ('js',os.path.join(PATH,'static/js').replace('\\','/') ), 
    ('img',os.path.join(PATH,'static/img').replace('\\','/') ), 
     os.path.join(PATH,'apps/upload_avatar/static').replace('\\','/'), 
     os.path.join(PATH,'apps/user_app/static').replace('\\','/'),
     os.path.join(PATH,'apps/user_app/static').replace('\\','/'),
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
     'middleware.filter_middleware.AuthenticationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django.middleware.cache.UpdateCacheMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'pinloveweb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pinloveweb.wsgi.application'

TEMPLATE_DIRS = (
     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.="/static/img/logo.png"/></a></d
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PATH,'templates').replace('\\','/'), 
    os.path.join(PATH,'apps/user_app/templates').replace('\\','/'), 
    os.path.join(PATH,'apps/upload_avatar/templates').replace('\\','/'), 
    os.path.join(PATH,'apps/recommend_app/templates').replace('\\','/'), 
    os.path.join(PATH,'apps/game_app/templates').replace('\\','/'), 
    os.path.join(PATH,'apps/verification_app/templates').replace('\\','/'),
    os.path.join(PATH,'apps/message_app/templates').replace('\\','/'),
    os.path.join(PATH,'apps/friend_dynamic_app/templates').replace('\\','/'), 
    os.path.join(PATH,'apps/third_party_login_app/templates').replace('\\','/'), 
)

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
    #监控memcahe
#     'django_memcached',
#     'social_auth',
#     'grappelli',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
#     'djcelery',   
#     'apps.task_app',     
)
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
        'custom_log_file':{
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PATH, 'logs/django.log').replace('\\','/'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216', # 16megabytes(16M)
            'formatter': 'verbose'
        },
        'django_request_logfile':{
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PATH, 'logs/django_request_logfile.log').replace('\\','/'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216', # 16megabytes(16M)
            'formatter': 'django_request'
        },
        'django_db_backends_logfile':{
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PATH, 'logs/django_db_backends_logfile.log').replace('\\','/'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
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
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins','django_request_logfile'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['django_db_backends_logfile','console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        
        'customapp': {#then you can change the level to control your custom app whether to output the debug infomation
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'customapp.engine': {#then you can change the level to control your custom app whether to output the debug infomation
            'handlers': ['custom_log_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
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
SESSION_COOKIE_AGE=1000
#缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT':0,
    },
}
from util.cache import init_cache
init_cache()
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
# MEDIA_ROOT = os.path.join(PATH,'update').replace('\\','/')
# STATIC_ROOT = os.path.join(PATH,'static').replace('\\','/')
# UPLOAD_AVATAR_UPLOAD_ROOT= os.path.join(PATH,'update/user_img').replace('\\','/')
# UPLOAD_AVATAR_AVATAR_ROOT= os.path.join(PATH,'update/user_img').replace('\\','/')
# UPLOAD_AVATAR_URL_PREFIX_ORIGINAL='/media/user_img/'
# UPLOAD_AVATAR_URL_PREFIX_CROPPED='/avatar/'



#---服务器环境-----
DATABASES = {
          
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pinlove_db_1',                      # Or path to database file if using sqlite3.
                                                # The following settings are not used with sqlite3:
        'USER': 'pinloveteam',
        'PASSWORD': 'redyellowblue#123',
        'HOST': '',                             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                             # Set to empty string for default.
    }
}
#upload 上传地址
MEDIA_URL = 'http://www.pinpinlove.com/update/'
MEDIA_ROOT ='/home/pinloveteam/webapps/pinlove/pinloveweb/update'
#静态文件地址
STATIC_ROOT = '/home/pinloveteam/webapps/pinlove_static'
STATIC_URL = 'http://www.pinpinlove.com/static/'
#头像上传地址
UPLOAD_AVATAR_UPLOAD_ROOT='/home/pinloveteam/webapps/pinlove/pinloveweb/update/user_img'
UPLOAD_AVATAR_AVATAR_ROOT='/home/pinloveteam/webapps/pinlove/pinloveweb/update/user_img'
UPLOAD_AVATAR_URL_PREFIX_ORIGINAL='/media/user_img/'
#grappelli
UPLOAD_AVATAR_URL_PREFIX_CROPPED='/avatar/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

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


