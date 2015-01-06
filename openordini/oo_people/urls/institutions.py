from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings

from open_municipio.urls import *
from open_municipio.om.views import HomeView
from openordini.oo_people.views import OOCommitteeDetailView, OOCouncilListView

# place app url patterns here
urlpatterns = patterns('',
	url(r'^committees/(?P<slug>[-\w]+)/$', OOCommitteeDetailView.as_view(), name='om_institution_committee'),
    url(r'^council/$', OOCouncilListView.as_view(), name='om_institution_council'),
)
