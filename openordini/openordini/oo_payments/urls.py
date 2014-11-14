from django.conf.urls.defaults import patterns, url, include

from .views import payment_details

urlpatterns = patterns('',
    url(r'^details/(?P<id>\d+)', payment_details, name='oo_payment_details'),
    url(r'', include('payments.urls')),
)
