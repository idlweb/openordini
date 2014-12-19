from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from open_municipio.users.models import User
from open_municipio.users.views import UserProfileDetailView
from open_municipio.people.models import municipality

from ..oo_payments.forms import PaymentForm
from ..oo_payments.models import SubscriptionPlan
from ..acts_fulfillments.models import Fascicolo
from .models import UserProfile

class OOUserProfileDetailView(UserProfileDetailView):

    model = UserProfile
 
    def get_object(self, queryset=None):
        user = self.request.user

        profile = None

        try:

            profile = user.get_profile()
        except (ObjectDoesNotExist, AttributeError):
            pass

        return profile
   
    def get_context_data(self, **kwargs):

        ctx = super(OOUserProfileDetailView, self).get_context_data(**kwargs)

        curr_person = None
        ctx["acts_facicoli"] = None

        try:
            curr_person = self.object.person

#            print "person: %s" % curr_person
            ctx["acts_fascicoli"]  = Fascicolo.objects.filter(recipient_set__person=curr_person)

        except (ObjectDoesNotExist, AttributeError), err:
            print "error: %s" % err


#        print "return ctx: %s" % ctx

        # add the payment form  
        user_charges = curr_person.userprofile.committee_charges

#        print "user charges: %s" % user_charges
    
        sub_codes = set()
        for curr_charge in user_charges:
#            print "curr charge institution: %s" % curr_charge.institution
            curr_code = settings.SUBSCRIPTION_COMMITTEE_MAPS.get(curr_charge.institution.slug, None)
            if curr_code:
                sub_codes.add(curr_code)

#        print "all payment codes: %s" % sub_codes
        plans = SubscriptionPlan.objects.filter(code__in=sub_codes)
        plan_choices = map(lambda p: (p.pk, p.name), plans)
#        print "plan choices: %s" % plan_choices
        ctx["form_payment"] = PaymentForm(choices=plan_choices)
        return ctx
