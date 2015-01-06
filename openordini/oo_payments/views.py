from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from payments import get_payment_model, RedirectNeeded

from decimal import Decimal

from datetime import date

from .models import SubscriptionOrder, Payment, SubscriptionPlan
from .forms import PaymentForm, PaymentInfoForm

class PaymentSucceed(TemplateView):
    template_name = 'oo_payments/succeed.html'

class PaymentError(TemplateView):
    template_name = 'oo_payments/error.html'

class PaymentReceipt(DetailView):
    
    template_name = 'oo_payments/payment_receipt.html'
    model = Payment
    

class PaymentInfo(FormView):
    template_name = 'oo_payments/payment_info.html'
    form_class = PaymentInfoForm

#    def get_success_url(self):
#        return reverse('oo_payment_details')

    def get_context_data(self, *args, **kwargs):

        ctx = super(PaymentInfo, self).get_context_data(*args, **kwargs)
#        print "in get context..."

        plan_pk = self.request.GET.get("payment_type")
        plan = SubscriptionPlan.objects.get(pk=plan_pk)
    
        # check plans are compatible with user profile
        user_plans = SubscriptionPlan.get_for_user(self.request.user)
        if plan not in user_plans:
            raise ValueError("The specified payment type (%s) is not allowed for user" % plan)
    
        ctx["plan"] = plan
#        print "ctx: %s" % ctx
        return ctx

    def get_form(self, *args, **kwargs):
    
        form = PaymentInfoForm(data=self.request.POST or None)
        form.fields["payment_type"].initial = self.request.GET.get("payment_type")
        return form

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

###<<<<<<< HEAD
    def form_valid(self, *args, **kwargs):
        year = date.today().year
    
        request = self.request
###=======
###def payment_details(request):
###
###    year = date.today().year
###
###    if not request.user.is_authenticated():
###        raise ValueError("You must be authenticated in order to access this view")
###
####    print "profile: %s (%s)" % (request.user.userprofile, type(request.user.userprofile))
###
###    profile = request.user.get_profile()
###    person = profile.person
###
###    if SubscriptionPlan.objects.all().count() == 0:
###        raise ValueError("You must have at least one SubscriptionPlan before calling this view")
###>>>>>>> master

        if not request.user.is_authenticated():
            raise ValueError("You must be authenticated in order to access this view")
    
        print "profile: %s (%s)" % (request.user.userprofile, type(request.user.userprofile))
    
        profile = request.user.get_profile()
        person = profile.person
    
        if SubscriptionPlan.objects.all().count() == 0:
            raise ValueError("You must have at least one SubscriptionPlan before calling this view")
    
        plan_pk = request.POST.get("payment_type")
        plan = SubscriptionPlan.objects.get(pk=plan_pk)
    
        # check plans are compatible with user profile
        user_plans = SubscriptionPlan.get_for_user(request.user)
        if plan not in user_plans:
            raise ValueError("The specified payment type (%s) is not allowed for user" % plan)
    
        order_defaults = {
            'plan': plan,
        }
    
        order, created = SubscriptionOrder.objects.get_or_create(
            person=person,
            date_begin='%s-01-01' % year,
            date_end='%s-12-31' % year,
            defaults = order_defaults
        )
    
        billing_address = request.POST.get("billing_address")
        billing_city = request.POST.get("city")
        billing_postcode = request.POST.get("postcode")
        customer_ip = self.get_client_ip(request)
    
        pay_default = {
            'variant':'default',
            'order': order,
            'description': order.name,
            'total': plan.total_amount,
            'tax': plan.tax,
            'delivery': Decimal(0),
            'billing_first_name': person.first_name,
            'billing_last_name': person.last_name,
            'billing_address_1': billing_address, 
            'billing_address_2':'',
            'billing_city': billing_city,
            'billing_postcode': billing_postcode,
            'billing_country_code':'IT',
            'billing_country_area':'',
            'customer_ip_address': customer_ip,
        }
    
        payment, created = Payment.objects.get_or_create(order=order, defaults=pay_default)

        

        print "passing id: %s" % payment.pk
        return HttpResponseRedirect(
            reverse('oo_payment_details', kwargs={"payment_id":payment.pk})
        )
            


def payment_details(request, payment_id, *args, **kwargs):

   
    try:
#        print "payment id: %s" % payment_id
        payment = Payment.objects.get(id=payment_id)
        plan = payment.order.subscriptionorder.plan
        form = payment.get_form(data=request.POST or None)

        ctx = {
            'form': form,
            'payment': payment,
            'plan': plan,
        }
    
        return TemplateResponse(request, 'oo_payments/payment.html', ctx)

    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    
