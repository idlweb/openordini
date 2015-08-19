# Create your views here.
from datetime import datetime

import logging

import json

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from django.core.exceptions import ObjectDoesNotExist
from open_municipio.people.views import PoliticianDetailView, CommitteeDetailView, \
                                        CouncilListView, CommitteeListView
from open_municipio.people.models import Institution, InstitutionCharge, Person, municipality
from open_municipio.people.views import PoliticianSearchView
from open_municipio.events.models import Event

from open_municipio.acts.models import Act
from open_municipio.users.models import UserProfile as UOM
from openordini.oo_users.models import UserProfile as UOO
from openordini.oo_users.models import Recapito
from openordini.oo_users.models import ExtraPeople 

from django.core import serializers

from sorl.thumbnail import get_thumbnail

from ..commons.mixins import FilterActsByUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import inspect  

class OOPoliticianDetailView(FilterActsByUser, PoliticianDetailView):

    def get_context_data(self, **kwargs):


        ctx = super(OOPoliticianDetailView, self).get_context_data(**kwargs)

        #... filtra ctx["presented_acts"] ...

        all_acts = Act.objects.filter(Q(actsupport__charge__pk__in=self.object.all_institution_charges) | Q(recipient_set__in=self.object.all_institution_charges))

        filtered_acts = self.filter_acts(all_acts, self.request.user).distinct()

        ctx["presented_acts"] = filtered_acts
        ctx["n_presented_acts"] = len(filtered_acts) 
        # per ricavare il campo descrizione da userprofile 

        #Slug = self.request.GET.get('slug')
        #print type(kwargs)
        #print type(kwargs).__dict__.items()
        #print kwargs.values()
        #print kwargs["person"]
        #print type(self.request)
        #print type(self.request).__dict__.items()
        """
        for key, value in kwargs.items():
            print(key, value)
        print  kwargs["object"].slug        
        """
        #print settings.COMMITTEE_SLUGS["psicologo_lavoro"]
        try:
            sUOO = UOO.objects.get(person__slug=kwargs["object"].slug)
            uRecapito = Recapito.objects.get(recapiti_psicologo = sUOO.pk)
            uExtraPeople = ExtraPeople.objects.get(anagrafica_extra = sUOO.pk)
            #print (uExtraPeople)
            ctx["iscrizione"] = sUOO.numero_iscrizione
            ctx["biografia"]  =  sUOO.description
            ctx["studio"]  =  uExtraPeople.denominazione_studio
            ctx["m_lat"] = uExtraPeople.coord_lat 
            ctx["m_long"] = uExtraPeople.coord_long 
            ctx["sito_internet"] = uRecapito.sito_internet
            ctx["indirizzo_email"] =  uRecapito.indirizzo_email
            ctx["indirizzo_pec"] = uRecapito.indirizzo_pec
            ctx["telefono_studio"] = uRecapito.tel_ufficio

        except:
            pass
                
        return ctx


class OOCommitteeDetailView(CommitteeDetailView):

    def get_context_data(self, **kwargs):
        # avoid calling super method, because it takes too long
        print "call super ..."
    
        # note: we don't call CommitteeDetailView.get_context_data(...) but
        # its super method; the code in CommitteeDetailView.get_context_data
        # is very slow
        ctx = super(CommitteeDetailView, self).get_context_data(**kwargs)

        # Are we given a real Committee institution as input? If no,
        # raise 404 exception.
        if self.object.institution_type != Institution.COMMITTEE:
            raise Http404

        committee_list = municipality.committees.as_institution()

        # fetch charges and add group
        president = self.object.president
        if president and president.charge.original_charge_id:
            president.group = InstitutionCharge.objects.current().select_related().\
                                  get(pk=president.charge.original_charge_id).council_group
        vicepresidents = self.object.vicepresidents
        for vp in vicepresidents:
            if vp and vp.charge.original_charge_id:
                vp.group = InstitutionCharge.objects.current().select_related().\
                    get(pk=vp.charge.original_charge_id).council_group

        members = self.object.members.order_by('person__last_name')


        resources = dict(
            (r['resource_type'], {'value': r['value'], 'description': r['description']})
                for r in self.object.resources.values('resource_type', 'value', 'description')
        )

        events = Event.objects.filter(institution=self.object)

        ctx["members"] = members
        ctx["object"] = self.object
        ctx["events"] = events
        ctx["committees"] = committee_list
        ctx["president"] = president
        ctx["vice_presidents"] = vicepresidents
        ctx["resources"] = resources

        ctx["current_site"] = Site.objects.get(pk=settings.SITE_ID)
        #ctx["members_for_pages"] = members_for_pages
#        members = self.object.sub_body_set.all()
#        print "members: %s" % members
#        paginator = Paginator(members, 20)
##        page = self.request.GET.get('page', 1)
##        try:
##            page_obj = paginator.page(page)
##        except PageNotAnInteger:
##            # If page is not an integer, deliver first page.
##            page_obj = paginator.page(1)
##        except EmptyPage:
##            # If page is out of range (e.g. 9999), deliver last page of results.
##            page_obj = paginator.page(paginator.num_pages)
##
##        ctx['paginator'] = paginator        
##        ctx['page_obj'] = page_obj
        ctx["sub_committees"] = self.object.sub_body_set.all()

        return ctx


class OOCommitteeListView(CommitteeListView):

    def get_context_data(self, **kwargs):
        ctx = super(OOCommitteeListView, self).get_context_data(**kwargs)
        
        ctx["current_site"] = Site.objects.get(pk=settings.SITE_ID)

        return ctx


class OOCouncilListView(FilterActsByUser, CouncilListView):

    def get_context_data(self, *args, **kwargs):

        ctx = super(OOCouncilListView, self).get_context_data(*args, **kwargs)

        all_acts = Act.objects.filter(
            emitting_institution__institution_type=Institution.COUNCIL
            ) #.order_by('-presentation_date')

        latest_acts = self.filter_acts(all_acts, self.request.user).distinct().order_by('-presentation_date')[0:3]
        
        ctx["latest_acts"] = latest_acts

        return ctx


class OOPoliticianSearchView(PoliticianSearchView):

    def get(self, request, *args, **kwargs):

        key = request.GET.get('key', '')
        ajax = request.GET.get('ajax', 0)
        max_rows = request.GET.get('max_rows', 10)


        current_site = Site.objects.get(pk=settings.SITE_ID)

        persons = Person.objects.\
            filter((Q(first_name__icontains=key) | Q(last_name__icontains=key) | Q(userprofile__userprofile__anagrafica__indirizzo_studio__icontains=key) | Q(userprofile__userprofile__anagrafica__citta_studio__icontains=key) | Q(userprofile__userprofile__anagrafica__cap_studio__icontains=key) | Q(userprofile__userprofile__anagrafica__denominazione_studio__icontains=key)) or (Q(first_name__icontains=key) and Q(last_name__icontains=key))).distinct()[0:max_rows]
        print "dalla select"
        print persons
        print "cio che arriva"
        # build persons array,substituting the img with a 50x50 thumbnail
        # and returning the absolute url of the thumbnail
    
        results = []
        for person in persons:

            try:
                img = get_thumbnail(person.img, "50x50", crop="center", quality=99)
                img_url = img.url
            except BaseException as e:
                img_url = "http://%s/static/img/placehold/face_50.png#%s" % (current_site, e)

 
            # manually build a dictionary to have more control on extra
            # data to show (i.e. data not from model Person)
            p_data = {
                "fields": { 
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "slug": person.slug,
                    "img": img_url,
                    "extra_data": "",
                }
            }      
            print "nome %s" % (person.first_name)
            print "cognome %s" % (person.last_name)
            #if person.userprofile and person.userprofile.userprofile: #and \
            if person.userprofile:
                    #person.userprofile.userprofile.anagrafica:
                #p_data["fields"]["extra_data"] = person.userprofile.userprofile.anagrafica.studio
                pass

            results.append(p_data)
            

        json_data = json.dumps(results)
        print "----------------------"
        print results

        return HttpResponse(json_data, mimetype='text/json')

