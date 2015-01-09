# Create your views here.
from datetime import datetime
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from haystack.query import SearchQuerySet

from open_municipio.om_search.forms import RangeFacetedSearchForm
from open_municipio.acts.views import ActDetailView, ActSearchView
from .models import Fascicolo

class FascicoloDetailView(ActDetailView):
    model = Fascicolo

    def get_object(self):

        user = self.request.user
        act = super(FascicoloDetailView, self).get_object()

#        print "user: %s, act: %s" % (user, act)

        if user.is_superuser:
            return act

        allowed_persons = map(lambda c: c.person, act.recipient_set.all())

#        print "allowed: %s" % allowed_persons
#        print "user: %s (%s)" % (user, user.is_anonymous())

        if user.is_anonymous():
#            print "it's anonymous..."
            raise PermissionDenied

#        print "non anonymous..."

        try:
            profile = user.get_profile()
#        print "profile: %s" % profile
            person = profile.person if profile else None
#        print "person: %s" % person

            if not person or person not in allowed_persons:
                raise PermissionDenied

        except ObjectDoesNotExist:
            raise PermissionDenied

        return act

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(FascicoloDetailView, self).dispatch(request, *args, **kwargs)
        except PermissionDenied, e:
#            print "error: %s" % e
            messages.warning(request, _("The act you are trying to access is visible only to a subset of the users. You may try to access as a different user, if you have other credentials."))
            base_url = reverse("auth_login")
            full_url = "%s?next=%s" % (base_url, request.path)
            return HttpResponseRedirect(full_url)


class OOActSearchView(ActSearchView):

    def __init__(self, *args, **kwargs):
        # dynamically compute date ranges for faceted search
        curr_year = datetime.today().year
        for curr_year in xrange(settings.OM_START_YEAR, curr_year + 1):
            date_range = self._build_date_range(curr_year)
            self.DATE_INTERVALS_RANGES[curr_year] = date_range

        sqs = SearchQuerySet().filter(django_ct='acts.act').\
            exclude(act_type='fascicolo').\
            facet('act_type').facet('is_key').facet('is_proposal').\
            facet('initiative').facet('organ').facet('month')

        for (year, range) in self.DATE_INTERVALS_RANGES.items():
            sqs = sqs.query_facet('pub_date', range['qrange'])
        sqs = sqs.order_by('-pub_date').highlight()
        kwargs['searchqueryset'] = sqs

        # Needed to switch out the default form class.
        if kwargs.get('form_class') is None:
            kwargs['form_class'] = RangeFacetedSearchForm

        super(ActSearchView, self).__init__(*args, **kwargs)

