from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

from django.conf import settings

from open_municipio.urls import *
#from sendgrid.urls import *
from sendgrid.views import listener

from .views import OOHomeView
from ..oo_users.forms import UserRegistrationForm
#from sendgrid.urls import *
#from sendgrid.views import listener

from ..oo_mese_benessere.admin import admin_site
#from rest_framework.authtoken.views import obtain_auth_token


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
    url(r"^events/$", "sendgrid.views.listener", name="sendgrid_post_event"),
    url(r'^benessere/', 'openordini.oo_mese_benessere.views.home'),
    url(r'^hacker/','openordini.oo_mese_benessere.views.login'),
    url(r'^/mbadminT/login/', 'openordini.oo_mese_benessere.views.request_per_login'),
    url(r'^mbadminT/', include(admin_site.urls)),
    url(r'^mbadmin/', 'openordini.oo_mese_benessere.views.mb_redirect'),#, include(admin_site.urls)),
    #url(r'^api/token/', obtain_auth_token, name='api-token')       
) + urlpatterns

