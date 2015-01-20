from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings

from open_municipio.urls import *
from open_municipio.om.views import HomeView
from openordini.oo_people.views import *

from .views import OOUserProfileDetailView, OOUserProfileListView, \
            OOUserProfileEditView, GenerateModuleSezA

# place app url patterns here
urlpatterns = patterns('',
    url(r'^$',
        OOUserProfileListView.as_view(),
       name='profiles_profile_list'),
	url(r'^profile/$', 
        OOUserProfileDetailView.as_view(), name='profiles_profile_detail'),
#    url(r'^profile/edit/$',
#        'profiles.views.edit_profile', name='profiles_edit_profile'),
    url(r'^profile/edit/$',
        OOUserProfileEditView.as_view(), name='profiles_edit_profile'),
    url(r'^profile/(?P<username>[\w\.@]+)/$', 
        OOUserProfileDetailView.as_view(), name='profiles_profile_detail'),

    url(r'^module/sez_a/$',
        GenerateModuleSezA.as_view(), name='profiles_module_subscribe_a'),
)
