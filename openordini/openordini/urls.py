from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings

from open_municipio.urls import *

from .views import OOHomeView
from ..oo_users.forms import UserRegistrationForm

urlpatterns = patterns('',

    url(r'^$', OOHomeView.as_view(), name="home"),

    # must override existing urls
    url(r'^accounts/register/$', register, {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': UserRegistrationForm,
        }, name='registration_register'),
    url(r'^accounts/login/$', 'django_cas_ng.views.login', name='auth_login'),
    url(r'^logout/$', 'django_cas_ng.views.logout', name='logout'),
	url('^people/', include('openordini.oo_people.urls')),
    url('^payments/', include('openordini.oo_payments.urls')),

    url(r'^cas/', include('mama_cas.urls')),

) + urlpatterns

