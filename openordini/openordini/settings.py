from open_municipio.settings import *
from openordini.cas_integration import CAS_populate_user

# root directory for this Django project (on the server machine)
MAIN_APP_ROOT = os.path.join(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(os.path.dirname(MAIN_APP_ROOT))
REPO_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))

DATABASES = {
    'default': {
    }
}

##AUTHENTICATION_BACKENDS = (
##    'django.contrib.auth.backends.ModelBackend',
##    'django.contrib.auth.backends.RemoteUserBackend',
##    'django_cas.backends.CASBackend',
##
##)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'django_cas.middleware.CASMiddleware',
)

TEMPLATE_LOADERS = (
    'apptemplates.Loader',
) + TEMPLATE_LOADERS

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
) + TEMPLATE_DIRS

INSTALLED_APPS = INSTALLED_APPS + (
    'mama_cas',
    'django_cas',
    'payments',   
    'open_municipio',
    'openordini.oo_payments',
    'openordini.cas_integration',
)

ROOT_URLCONF = 'openordini.openordini.urls'

MEDIA_ROOT = os.path.join(REPO_ROOT, 'public', 'media')
STATIC_ROOT = os.path.join(REPO_ROOT, 'public', 'static')

STATIC_URL = "/static/"


STATICFILES_DIRS = (
    os.path.join(MAIN_APP_ROOT, 'static'),
) + STATICFILES_DIRS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'console-import':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename': os.path.join(REPO_ROOT,"log","logfile"),
            'formatter': 'standard',
            },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'webapp': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename': REPO_ROOT + "/log/webapp.log",
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'import': {
            'handlers': ['console-import', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'webapp': {
            'handlers': [ 'webapp', ],
            'level': 'DEBUG',
            'propagate': True,
            }, 
                
    }
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

PAYMENT_BASE_URL = 'http://localhost:8000/'

PAYMENT_MODEL = 'oo_payments.Payment'

PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {})}

SUBSCRIPTION_MAPS = {
    'FIRST': ("STUD", ),
    'ALL': ("PSCH", "PSLG",)
}

CAS_IGNORE_REFERER = False
CAS_LOGOUT_COMPLETELY = True
CAS_SERVER_URL = '' # this MUST be set in your deploy settings
CAS_GATEWAY_PARAMETER = "gateway"
CAS_GATEWAY_LOOP_PARAMETER = "gateway"
CAS_USER_DETAILS_RESOLVER = CAS_populate_user

# override registration configuration
REGISTRATION_AUTO_LOGIN = True
AUTH_PROFILE_MODULE = 'oo_users.UserProfile'

REGISTRATION_GROUP_MEMBERS_AUTO = True
GROUP_PSICOLOGO_FORENSE = "psicologi forensi"
GROUP_PSICOLOGO_LAVORO = "psicologi del lavoro"
GROUP_PSICOLOGO_CLINICO = "psicologi clinici"
