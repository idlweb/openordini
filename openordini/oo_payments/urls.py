from django.conf.urls.defaults import patterns, url, include

from .views import payment_details, PaymentSucceed, PaymentError

urlpatterns = patterns('',
    url(r'^details/', payment_details, name='oo_payment_details'),
    url(r'^succeed/', PaymentSucceed.as_view(), name='oo_payment_succeed'),
    url(r'^error/', PaymentError.as_view(), name='oo_payment_error'),
    url(r'', include('payments.urls')),
)
