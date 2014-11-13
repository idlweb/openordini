from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings


from open_municipio.urls import *


urlpatterns += patterns('',
    url('^payments/', include('payments.urls')),
)
