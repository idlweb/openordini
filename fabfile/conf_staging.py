import os

# IP/domain name of the staging server
SERVER_MACHINE = '5.249.143.113' ## CHANGEME!
# Python interpreter executable to use on virtualenv creation
PYTHON_BIN = 'python' #pyhton 2.7
PYTHON_PREFIX = '' # e.g. ``/usr``, ``/usr/local``; leave empty for default.
PYTHON_FULL_PATH = "%s/bin/%s" % (PYTHON_PREFIX, PYTHON_BIN) if PYTHON_PREFIX else PYTHON_BIN
# exclude patterns for ``rsync`` invocations
RSYNC_EXCLUDE = ( 
    '*~',
    '*.pyc',
    'settings_*.py',
    'urls_*.py',
)
# the name of the Django project managed by this fabfile
PROJECT_NAME = 'openordini' ## CHANGEME!
# a unique identifier for this web application instance
# usually it's set to the primary domain from which the web application is accessed
APP_DOMAIN = 'oo.psicologipuglia.it' ## CHANGEME!
# filesystem location of project's repository on the local machine
LOCAL_REPO_ROOT =  os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
# filesystem location of Django project's files on the local machine
LOCAL_PROJECT_ROOT = os.path.join(LOCAL_REPO_ROOT, PROJECT_NAME) 
# system user (on the server machine) used for managing files 
# shared between OpenOrdini's instances
WEB_USER = 'oo'
# absolute filesystem path to the public SSH key being used 
# to login as ``WEB_USER`` on the remote machine(s)
WEB_USER_HOSTKEY = '~/.ssh/id_rsa.pub' ## CHANGEME!
# system user (on the server machine) used for managing this OpenOrdini's instance
OM_USER = WEB_USER 
# absolute filesystem path to the public SSH key being used 
# to login as the ``OM_USER`` user on the remote machine(s)
OM_USER_HOSTKEY = WEB_USER_HOSTKEY 
###------------------  Django ------------###
# the parent directory of domain-specific directories (on the server machine) 
WEB_ROOT = '/home/oo'
# the root directory for domain-specific files (on the server machine)
DOMAIN_ROOT = os.path.join(WEB_ROOT, APP_DOMAIN) 
# the root directory of application-specific Python virtual environment (on the server machine)
VIRTUALENV_ROOT = os.path.join(DOMAIN_ROOT, 'private', 'venv') 
# the root directory for project-specific files (on the server machine)
PROJECT_ROOT = os.path.join(DOMAIN_ROOT, 'private', PROJECT_NAME)
# import path of Django settings module for the staging environment
DJANGO_SETTINGS_MODULE = '%(project)s.%(project)s.settings_staging' % {'project': PROJECT_NAME}
# Directory where static files should be collected.  This MUST equal the value
# of ``STATIC_ROOT`` attribute of the Django settings module used on the server.
STATIC_ROOT =  os.path.join(DOMAIN_ROOT, 'public', 'static')
###------------------  Tomcat ------------###
# system user the Tomcat process run as 
TOMCAT_USER = 'tomcat6'
# Tomcat's controller script 
TOMCAT_CONTROLLER = '/etc/init.d/tomcat6'
# home dir for Catalina
CATALINA_HOME = '/etc/tomcat6/Catalina'
###------------------  Solr ------------###
# absolute filesystem path to the public SSH key being used 
# to login as the ``solr`` user on the remote machine(s)
SOLR_USER_HOSTKEY = '~/.ssh/id_rsa.pub' ## CHANGEME!
# URL pointing to the Solr distribution to be installed on the server machine
# Must be a compressed tarball (i.e. a  ``.tgz`` or ``.tar.gz`` file)
SOLR_DOWNLOAD_LINK = 'https://archive.apache.org/dist/lucene/solr/3.6.1/apache-solr-3.6.1.tgz'
# where Solr configuration and data reside on the server machine
SOLR_INSTALL_DIR = '/home/apache-solr-3.6.1'
# where configuration/data files for Solr reside on the server machine
SOLR_HOME = '/home/solr'
###------------------  PostgreSQL ------------###
# root dir for PostgreSQL configuration files
POSTGRES_CONF_DIR = '/etc/postgresql/9.1/main'
# PostgreSQL's controller script 
POSTGRES_CONTROLLER = 'service postgresql'
# DB username
DB_USER = OM_USER 
# name of the application DB
DB_NAME = PROJECT_NAME
PROVISION_PACKAGES = ['mercurial',
                      'python-dev',
                      'libxml2', 
                      'libxml2-dev', 
                      'libxslt1.1', 
                      'libxslt-dev',
                      'postgresql-server-dev-9.1',
                      'python-virtualenv',   
                      'git',
                      'nginx',
                     ]

