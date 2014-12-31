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

        profile = None
        user = self.request.user

        url_username = self.kwargs.get("username", None)

        try:
            if url_username:
                user = User.objects.get(username=url_username)
            
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


        """ 
        map: data una funzione ed una sequenza 
        applica quella funzione ad agni elemento 
        della sequenza 
        """
        plans = SubscriptionPlan.get_for_user(self.request.user)
        plan_choices = []

        if plans:
            plan_choices = map(lambda p: (p.pk, p.name), plans)

#        print "plan choices: %s" % plan_choices
        ctx["form_payment"] = PaymentForm(choices=plan_choices)
        return ctx
