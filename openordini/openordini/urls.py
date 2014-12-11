from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings
from django_cas.decorators import login_required

from open_municipio.urls import *
from open_municipio.om.views import HomeView

##class OOHomeView(HomeView):
##
##    def get(self, *args, **kwargs):
##        return super(OOHomeView, self).get(*args, **kwargs)
##
##
urlpatterns = patterns('',

#    url(r'^$', OOHomeView.as_view(), name='home'),
    # must override existing urls
    url(r'^accounts/login/$', 'django_cas.views.login', name='auth_login'),
    url(r'^logout/$', 'django_cas.views.logout', name='logout'),
) + urlpatterns

urlpatterns += patterns('',
	url('^people/', include('openordini.oo_people.urls')),
    url('^payments/', include('openordini.oo_payments.urls')),
) + urlpatterns

urlpatterns += patterns('', (r'^cas/', include('mama_cas.urls')))

#urlpatterns += patterns('', url(r'^grappelli/', include('grappelli.urls'))) # grappelli URLS

