from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings

from open_municipio.urls import *
from open_municipio.om.views import HomeView
from .views import FascicoloDetailView, OOActSearchView

# place app url patterns here
urlpatterns = patterns('',
    url(r'^$', OOActSearchView(template='acts/act_search.html'), name='om_act_search'),
	url(r'^fascicolo/(?P<slug>[-\w]+)/$', FascicoloDetailView.as_view(), name='oo_fascicolo_detail'),
    url(r'^fascicolo/(?P<slug>[-\w]+)/(?P<tab>documents)/$', FascicoloDetailView.as_view(), name='om_fascicolo_detail_documents'),
)
