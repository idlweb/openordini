from open_municipio.settings import *

# root directory for this Django project (on the server machine)
MAIN_APP_ROOT = os.path.join(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(os.path.dirname(MAIN_APP_ROOT))
REPO_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))

DATABASES = {
    'default': {
    }
}

TEMPLATE_LOADERS = (
    'apptemplates.Loader',
) + TEMPLATE_LOADERS

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
) + TEMPLATE_DIRS

INSTALLED_APPS = (
    #'wpadmin',
    'suit',
    #'grappelli',
    ) + INSTALLED_APPS + (
#INSTALLED_APPS += (
    'payments',   
    'open_municipio',
    'openordini.oo_payments',
    'openordini.cas_integration',  
    'openordini.acts_fulfillments',  
    'openordini.oo_people',
    'openordini.oo_users',
    'openordini.openordini',
    'awesome_bootstrap',
    'endless_pagination',
    'openordini.utility',
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
        'mama_cas.forms': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': True,
            },
        'mama_cas.mixins': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': True,
            },               
    }
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

PAYMENT_BASE_URL = '' # 'http://localhost:8000/'

PAYMENT_MODEL = 'oo_payments.Payment'

PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {})
}

# override registration configuration
REGISTRATION_AUTO_LOGIN = True
AUTH_PROFILE_MODULE = 'oo_users.UserProfile'

REGISTRATION_AUTO_ADD_GROUP = True
SYSTEM_GROUP_NAMES = {
    "psicologo_lavoro": "psicologi del lavoro",
    "psicologo_clinico": "psicologi clinici",
    "psicologo_forense": "psicologi forensi",
    "dottore_tecniche_psicologiche": "dottori tecniche psicologiche",
}

COMMITTEE_SLUGS = {
    "psicologo_lavoro": "sezione-a",
    "psicologo_clinico": "sezione-a",
    "psicologo_forense": "sezione-a",
    "dottore_tecniche_psicologiche": "sezione-b",
}

SITE_INFO = {
    'main_city': u'NPOP',
    'site_version': u'Beta',
    'main_city_logo': 'img/city-logo/city-logo.png',
    'main_city_website': 'http://www.psicologipuglia.it',
}

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Nuovo portale degli psicologi',
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    'MENU_ICONS': {
        'sites': 'icon-leaf',
        'auth': 'icon-lock',
    },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    'MENU_EXCLUDE': ('auth.group',),
     'MENU': (
        {'app': 'oo_users', 'label': 'Schede psicologi', 'icon':'icon-user', 'models': ('userprofile','extrapeople', 'recapito','psicologotitoli','caratteristiche_gestione','trasferimento')},
        {'app': 'people', 'label': 'Soggetti collegati', 'icon':'icon-user', 'models': ('person','office','institution','group','company','sitting')},       
        {'app': 'acts', 'label': 'Gestione atti del Consiglio', 'icon':'icon-book', 'models': ('act','deliberation','interrogation','interpellation','motion','agenda','amendment','transition','document','attach','speech','calendar')},
        {'app': 'acts_fulfillments', 'label': 'Fascicoli iscritti', 'icon':'icon-book', 'models': ('fascicolo')},
        {'app': 'oo_payments', 'label': 'Pagamenti', 'icon':'icon-tag', 'models': ('order','payment','subscriptionorder','subscriptionplan')},
        {'app': 'newsletter', 'label': 'Newsletter', 'icon':'icon-comment', 'models': ('newsletter')},
        {'app': 'attendances', 'label': 'Presenze', 'icon':'icon-check', 'models': ('attendance','chargeattendance')},
        {'app': 'events', 'label': 'Eventi', 'icon':'icon-calendar', 'models': ('event')},       
         'sites',         
        {'label': 'Impostazioni', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
         #{'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    ),

    # misc
    # 'LIST_PER_PAGE': 15
}

PAYMENT_DEADLINES = {
    "rinnovo-iscrizione": "%s-02-15",
}

MODULES_ROOT = "rtf"

MODULES = {
    "sez_a_uomo": os.path.join(MODULES_ROOT, "domanda_sez_a_u.rtf"), 
    "sez_a_donna": os.path.join(MODULES_ROOT, "domanda_sez_a_d.rtf"), 
}
