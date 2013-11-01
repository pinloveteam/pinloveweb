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
# # 本地环境----
# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#          'NAME': 'django',                      # Or path to database file if using sqlite3.
#                                                  # The following settings are not used with sqlite3:
#          'USER': 'root',
#          'PASSWORD': 'jin521436',
#          'HOST': '',                             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#          'PORT': '',                             # Set to empty string for default.
#      }
#  }
 
 


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
 
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
#---本地环境-----
# MEDIA_URL = '/media/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# # 本地环境-----
# MEDIA_ROOT = os.path.join(PATH,'update').replace('\\','/')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
# #---本地环境-----
# STATIC_ROOT = os.path.join(PATH,'static').replace('\\','/')
# 
# # URL prefix for static files.
# # Example: "http://example.com/static/", "http://static.example.com/"
# # 本地环境-----
# STATIC_URL = '/static/'


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
SECRET_KEY = 'zjz*z3^c@s@ay70o!$)8%f%y395_=$p5^*z$tlu_+j6$4ga!5+'

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
#     'apps.middleware.QtsAuthenticationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
    'grappelli',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
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


# upload the head portrait
#---本地环境-----
UPLOAD_AVATAR_UPLOAD_ROOT='D:\\eclipse\\code\\pinloveweb\\update\\user_img'
UPLOAD_AVATAR_AVATAR_ROOT='D:\\eclipse\\code\\pinloveweb\\update\\user_img'
UPLOAD_AVATAR_URL_PREFIX_ORIGINAL='/media/user_img/'
UPLOAD_AVATAR_URL_PREFIX_CROPPED='/avatar/'

#logging 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"


#---服务器环境-----
# DATABASES = {
#    
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'pinlove_db_1',                      # Or path to database file if using sqlite3.
#                                                 # The following settings are not used with sqlite3:
#         'USER': 'pinloveteam',
#         'PASSWORD': 'redyellowblue#123',
#         'HOST': '',                             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': '',                             # Set to empty string for default.
#     }
# }
MEDIA_URL = 'http://www.pinpinlove.com/update/'
MEDIA_ROOT ='/home/pinloveteam/webapps/pinlove/pinloveweb/update'
STATIC_ROOT = '/home/pinloveteam/webapps/pinlove_static'
STATIC_URL = 'http://www.pinpinlove.com/static/'
UPLOAD_AVATAR_UPLOAD_ROOT='/home/pinloveteam/webapps/pinlove/pinloveweb/update/user_img'
UPLOAD_AVATAR_AVATAR_ROOT='/home/pinloveteam/webapps/pinlove/pinloveweb/update/user_img'
UPLOAD_AVATAR_URL_PREFIX_ORIGINAL='/media/user_img/'
UPLOAD_AVATAR_URL_PREFIX_CROPPED='/avatar/'

