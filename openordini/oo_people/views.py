# Create your views here.
from datetime import datetime

import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from django.core.exceptions import ObjectDoesNotExist
from open_municipio.people.views import PoliticianDetailView, CommitteeDetailView, \
                                        CouncilListView
from open_municipio.people.models import Institution
from open_municipio.acts.models import Act
from django.core import serializers

from sorl.thumbnail import get_thumbnail

from ..commons.mixins import FilterActsByUser

class OOPoliticianDetailView(FilterActsByUser, PoliticianDetailView):

    def get_context_data(self, **kwargs):


        ctx = super(OOPoliticianDetailView, self).get_context_data(**kwargs)

        #... filtra ctx["presented_acts"] ...

        all_acts = Act.objects.filter(Q(actsupport__charge__pk__in=self.object.all_institution_charges) | Q(recipient_set__in=self.object.all_institution_charges))

        filtered_acts = self.filter_acts(all_acts, self.request.user)

        ctx["presented_acts"] = filtered_acts
        ctx["n_presented_acts"] = len(filtered_acts)

        return ctx


class OOCommitteeDetailView(CommitteeDetailView):

    def get_context_data(self, **kwargs):
        ctx = super(OOCommitteeDetailView, self).get_context_data(**kwargs)

        ctx["sub_committees"] = self.object.sub_body_set.all()

        return ctx


class OOCouncilListView(FilterActsByUser, CouncilListView):

    def get_context_data(self, *args, **kwargs):

        ctx = super(OOCouncilListView, self).get_context_data(*args, **kwargs)

        all_acts = Act.objects.filter(
            emitting_institution__institution_type=Institution.COUNCIL
            ) #.order_by('-presentation_date')

        latest_acts = self.filter_acts(all_acts, self.request.user).order_by('-presentation_date')[0:3]
        
        ctx["latest_acts"] = latest_acts

        return ctx

