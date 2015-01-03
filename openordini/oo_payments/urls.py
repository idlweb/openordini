from django.conf.urls.defaults import patterns, url, include

from .views import payment_details, PaymentSucceed, PaymentError, PaymentInfo, \
                                PaymentReceipt

urlpatterns = patterns('',
    url(r'^info/', PaymentInfo.as_view(), name='oo_payment_info'),
    url(r'^details/(?P<payment_id>[0-9]+)/', payment_details, name='oo_payment_details'),   
    url(r'^receipt/(?P<pk>[0-9]+)/', PaymentReceipt.as_view(), name='oo_payment_receipt'),

    url(r'^succeed/', PaymentSucceed.as_view(), name='oo_payment_succeed'),
    url(r'^error/', PaymentError.as_view(), name='oo_payment_error'),
    url(r'', include('payments.urls')),
)
