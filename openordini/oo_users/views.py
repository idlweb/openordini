from django.core.exceptions import ObjectDoesNotExist
from open_municipio.users.views import UserProfileDetailView

from ..acts_fulfillments.models import Fascicolo

class OOUserProfileDetailView(UserProfileDetailView):
    
    def get_context_data(self, **kwargs):

        ctx = super(OOUserProfileDetailView, self).get_context_data(**kwargs)

        curr_person = None
        ctx["acts_facicoli"] = None

        try:
            curr_person = self.object.person

            print "person: %s" % curr_person
            ctx["acts_fascicoli"]  = Fascicolo.objects.filter(recipient_set__person=curr_person)

        except (ObjectDoesNotExist, AttributeError), err:
            print "error: %s" % err


        print "return ctx: %s" % ctx
        return ctx
