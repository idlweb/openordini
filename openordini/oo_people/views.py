# Create your views here.
from datetime import datetime

import logging

from django.conf import settings
from django.contrib.sites.models import Site
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
		if self.request.user == User.objects.get(self.kwargs["slug"]):
			
			final_acts = []
				
			for act in ctx["presented_acts"]:

			    	if isinstance(act, Fascicolo): 
		
			    		continue
		
				final_acts.append(act)

			ctx["presented_acts"] = final_acts
			
		return ctx


