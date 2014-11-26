from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from payments import get_payment_model, RedirectNeeded

from decimal import Decimal

from datetime import date

from .models import SubscriptionOrder, Payment, SubscriptionPlan

class PaymentSucceed(TemplateView):
    template_name = 'oo_payments/succeed.html'

class PaymentError(TemplateView):
    template_name = 'oo_payments/error.html'

def payment_details(request):

    year = date.today().year

    if not request.user.is_authenticated():
        raise ValueError("You must be authenticated in order to access this view")

#    print "profile: %s" % request.user.userprofile

    person = request.user.userprofile.person

    if SubscriptionPlan.objects.all().count() == 0:
        raise ValueError("You must have at least one SubscriptionPlan before calling this view")

    order_defaults = {
        'plan': SubscriptionPlan.objects.all()[0]
    }

    order, created = SubscriptionOrder.objects.get_or_create(
        person=person,
        date_begin='%s-01-01' % year,
        date_end='%s-12-31' % year,
        defaults = order_defaults
    )

    pay_default = {
        'variant':'default',
        'order': order,
        'description': order.name,
        'total':Decimal(100),
        'tax':Decimal(20),
        'delivery':Decimal(120),
        'billing_first_name':person.first_name,
        'billing_last_name':person.last_name,
        'billing_address_1':'address',
        'billing_address_2':'',
        'billing_city':'city',
        'billing_postcode':'01234',
        'billing_country_code':'IT',
        'billing_country_area':'',
        'customer_ip_address':'192.168.0.1',
    }

    payment, created = Payment.objects.get_or_create(order=order, defaults=pay_default)
    
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'oo_payments/payment.html',
                            {'form': form, 'payment': payment})
    
