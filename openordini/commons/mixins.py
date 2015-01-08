from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.db.models import Q

from openordini.acts_fulfillments.models import Fascicolo
from open_municipio.monitoring.models import Monitoring

class FilterActsByUser(object):
    
    def filter_acts(self, acts, user):
    
        assert isinstance(acts, QuerySet) == True , ("Expected QuerySet, Passed %s, instead" % type(acts))

        if user.is_superuser:
            return acts

        # filter here

        all_charges = []

#        print "user charges: %s" % all_charges

        try:
            all_charges = user.get_profile().person.all_institution_charges
        except (ObjectDoesNotExist, AttributeError):
            pass

        return acts.filter(Q(fascicolo=None) | Q(recipient_set__in=all_charges))


class FilterNewsByUser(object):

    def filter_news(self, news, user):

        assert isinstance(news, QuerySet)

        if user.is_superuser:
            return news

        # filter here

        person = None
        my_acts = []

        try:
            person = user.get_profile().person
        except (ObjectDoesNotExist, AttributeError):
            pass

#        print "person: %s" % person

        ct = ContentType.objects.get_for_model(Fascicolo)

        # TODO fix: not working properly...
        my_acts = Fascicolo.objects.filter(recipient_set__person=person)

#        print "person acts: %s" % my_acts

        monitored_acts = Monitoring.objects.filter((~ Q (content_type=ct)) | Q(object_pk__in=my_acts))

#        print "monitored acts: %s" % monitored_acts

        m_ct = ContentType.objects.get_for_model(Monitoring)
    
        return news.filter((~ Q(generating_content_type=m_ct)) | Q(generating_object_pk__in=monitored_acts))
