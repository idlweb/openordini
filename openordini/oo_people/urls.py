from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings
from django_cas.decorators import login_required

from open_municipio.urls import *
from open_municipio.om.views import HomeView
from openordini.oo_people.views import *

# place app url patterns here
urlpatterns = patterns('',
	url(r'^(?P<slug>[-\w]+)/$', OOPoliticianDetailView.as_view(), name='om_politician_detail'),
)