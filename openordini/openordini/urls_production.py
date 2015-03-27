from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings


from openordini.openordini.urls import *

urlpatterns =  patterns('',
    url(r'^accounts/login/$', 'django_cas_ng.views.login', name='auth_login'),
    url(r'^accounts/logout/$', 'django_cas_ng.views.logout', name='logout'),
    url(r'^cas/', include('mama_cas.urls')),

) + urlpatterns
