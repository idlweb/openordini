from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

from django.conf import settings

from open_municipio.urls import *
from sendgrid.urls import *
from sendgrid.views import listener

from .views import OOHomeView
from ..oo_users.forms import UserRegistrationForm
#from sendgrid.urls import *
#from sendgrid.views import listener

admin.site.login = login_required(admin.site.login)

urlpatterns = patterns('',

    # url(r'^grappelli/', include('grappelli.urls')),

    url(r'^$', OOHomeView.as_view(), name="home"),

    # must override existing urls
    url(r'^accounts/register/$', register, {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': UserRegistrationForm,
        }, name='registration_register'),

    url('^acts/', include('openordini.acts_fulfillments.urls')),
	url('^people/', include('openordini.oo_people.urls.people')),
    url('^institutions/', include('openordini.oo_people.urls.institutions')),
    url('^users/', include('openordini.oo_users.urls')),
    url('^payments/', include('openordini.oo_payments.urls')),
) + urlpatterns

