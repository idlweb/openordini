from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings

from open_municipio.urls import *
from open_municipio.om.views import HomeView
from open_municipio.people.views import PoliticianListView

from openordini.oo_people.views import OOPoliticianSearchView, OOPoliticianDetailView

# I must include all the urlpatterns from OpenMunicipio, in order not to override
# the search url with the OOPoliticianDetailView <slug>
urlpatterns = patterns('',
    url(r'^$', PoliticianListView.as_view(), name='om_politician_list'),
    url(r'^search/$', OOPoliticianSearchView.as_view(), name='om_politician_search'),
	url(r'^(?P<slug>[-\w]+)/$', OOPoliticianDetailView.as_view(), name='om_politician_detail'),
)
