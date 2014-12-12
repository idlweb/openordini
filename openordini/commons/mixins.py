
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet

class FilterActsByUser(object):
    
    def filter_acts(self, acts, user):
    
        assert isinstance(acts, QuerySet)

        if user.is_superuser:
            return acts

        # filter here

        all_charges = []

        print "user charges: %s" % all_charges

        try:
            all_charges = user.get_profile().person.all_institution_charges
        except (ObjectDoesNotExist, AttributeError):
            pass

        return acts.filter(Q(fascicolo=None) | Q(recipient_set__in=all_charges))
