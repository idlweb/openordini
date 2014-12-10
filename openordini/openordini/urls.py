from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings

from open_municipio.urls import *

from ..oo_users.forms import UserRegistrationForm

urlpatterns = patterns('',

    # must override existing urls
    url(r'^accounts/register/$', register, {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': UserRegistrationForm,
        }, name='registration_register'),
    url(r'^accounts/login/$', 'django_cas_ng.views.login', name='auth_login'),
    url(r'^logout/$', 'django_cas_ng.views.logout', name='logout'),
) + urlpatterns

urlpatterns += patterns('',
    url('^payments/', include('openordini.oo_payments.urls')),
)

urlpatterns += patterns('', (r'^cas/', include('mama_cas.urls')))

