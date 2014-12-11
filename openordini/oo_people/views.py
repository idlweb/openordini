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
from open_municipio.people.views import PoliticianDetailView
from django.core import serializers

from sorl.thumbnail import get_thumbnail

class OOPoliticianDetailView(PoliticianDetailView):

    def get_context_data(self, **kwargs):


        ctx = super(OOPoliticianDetailView, self).get_context_data(**kwargs)

        #... filtra ctx["presented_acts"] ...

        print "ctx before: %s" % ctx

        if self.request.user.is_superuser:
            return ctx

        url_slug = self.kwargs["slug"]
        curr_profile = None

        try:
            curr_profile = self.request.user.get_profile()
        except ObjectDoesNotExist:
            pass

        if curr_profile and curr_profile.person and \
                curr_profile.person.slug == url_slug:
            
            final_acts = []
                
            for act in ctx["presented_acts"]:

                if isinstance(act, Fascicolo): 
                    continue
        
                final_acts.append(act)

            ctx["presented_acts"] = final_acts
            
        return ctx


