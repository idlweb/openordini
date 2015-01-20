import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import View
from open_municipio.users.models import User
from open_municipio.users.views import UserProfileDetailView, UserProfileListView, \
                                        extract_top_monitored_objects
from open_municipio.people.models import municipality, Person
from open_municipio.newscache.models import News
from open_municipio.acts.models import Deliberation, Interpellation, Interrogation, Agenda, Motion, Amendment

from ..oo_payments.forms import PaymentForm
from ..oo_payments.models import SubscriptionPlan, SubscriptionOrder
from ..acts_fulfillments.models import Fascicolo
from .models import UserProfile, ExtraPeople, Recapito
from .forms import UserProfileForm

from ..commons.mixins import FilterNewsByUser

class OOUserProfileDetailView(FilterNewsByUser, UserProfileDetailView):

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
#            pass
            raise Http404

        return profile
   
    def get_context_data(self, **kwargs):

        ctx = super(OOUserProfileDetailView, self).get_context_data(**kwargs)

        curr_person = None
        ctx["acts_facicoli"] = None

        try:
            curr_person = self.object.person

#            print "person: %s" % curr_person
            ctx["acts_fascicoli"]  = Fascicolo.objects.filter(recipient_set__person=curr_person) 

            curr_year = datetime.today().year

            ctx["curr_subscription"] = SubscriptionOrder.get_for_person(curr_person, curr_year)

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


        all_news = self.object.related_news
        filtered_news = self.filter_news(all_news, self.request.user)

#        print "all news: %s" % all_news
#        print "filtered news: %s" % filtered_news

        ctx["profile_news"] = sorted(filtered_news, key=lambda n: n.news_date, reverse=True)[0:3]


        return ctx


class OOUserProfileListView(FilterNewsByUser, UserProfileListView):
    
    def get_context_data(self, **kwargs):


#        print "in custom view ..."

        ctx = super(OOUserProfileListView, self).get_context_data(**kwargs)
    
        news = News.objects.filter(news_type=News.NEWS_TYPE.community, priority=1)
        filtered_news = self.filter_news(news, self.request.user)

        ctx["news_community"] = sorted(filtered_news, key=lambda n: n.news_date,
                                reverse=True)[0:3]

        # below it is not possible to use the mixin method filter_acts because
        # extract_top_monitored_objects does not return a QuerySet

        all_acts = extract_top_monitored_objects(Deliberation, Motion, 
                        Interpellation, Agenda, Interrogation, Amendment, Fascicolo, qnt=5)

        ctx["top_monitored_acts"] = self.filter_monitored_acts(all_acts)

        return ctx



    def filter_monitored_acts(self, all_acts):

        person = None

        try:
            person = self.request.user.get_profile().person
        except Exception:
            pass

        filtered_acts = []
        for curr_row in all_acts:


            if isinstance(curr_row["object"], Fascicolo):
                if not person:
                    # user has no associated person: don't show the Fascicolo
                    continue

                # otherwise check against recipients
                recipient_people = map(lambda c: c.person, curr_row["object"].recipients)
#                print "recipient people: %s" % recipient_people
#                print "person: %s" % person
                if person not in recipient_people:                
                    # person not in Fascicolo recipients
#                    print "person not found ..."
                    continue    

            filtered_acts.append(curr_row)

        return filtered_acts


class OOUserProfileEditView(FormView):

    form_class = UserProfileForm

    template_name = 'profiles/edit_profile.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("profiles_profile_detail")

    def get_initial(self):
        initial = super(OOUserProfileEditView, self).get_initial()

        user = self.request.user

        profile = user.get_profile()

#        print "profile: %s" % profile

        initial["location"] = profile.location
        initial["description"] = profile.description
        initial["image"] = profile.image
        initial["uses_nickname"] = profile.uses_nickname

        try:
    
            initial["indirizzo_residenza"] = profile.anagrafica.indirizzo_residenza
            initial["citta_residenza"] = profile.anagrafica.citta_residenza
            initial["cap_residenza"] = profile.anagrafica.cap_residenza
            initial["provincia_residenza"] = profile.anagrafica.provincia_residenza

            initial["indirizzo_domicilio"] = profile.anagrafica.indirizzo_domicilio
            initial["citta_domicilio"] = profile.anagrafica.citta_domicilio
            initial["cap_domicilio"] = profile.anagrafica.cap_domicilio
            initial["provincia_domicilio"] = profile.anagrafica.provincia_domicilio

        except ObjectDoesNotExist:
            pass

        try:
            initial["tel_residenza"] = profile.recapiti.tel_residenza
            initial["tel_domicilio"] = profile.recapiti.tel_domicilio
            initial["tel_ufficio"] = profile.recapiti.tel_ufficio
            initial["tel_cellulare"] = profile.recapiti.tel_cellulare
            initial["indirizzo_email"] = profile.recapiti.indirizzo_email or profile.user.email
            initial["indirizzo_pec"] = profile.recapiti.indirizzo_pec
        except ObjectDoesNotExist:
            initial["indirizzo_email"] = profile.user.email


        return initial


    def form_valid(self, form):

#        print "form valid ..."

#        print "data: %s" % form.cleaned_data

        # save data
        
        user = self.request.user

        profile = user.get_profile()

        profile.location = form.cleaned_data["location"]
        profile.description = form.cleaned_data["description"]
        profile.image = form.cleaned_data["image"]
        profile.uses_nickname = form.cleaned_data["uses_nickname"]

        profile.save()

        anagrafica, created = ExtraPeople.objects.get_or_create(anagrafica_extra=profile)

        anagrafica.indirizzo_residenza = form.cleaned_data["indirizzo_residenza"]
        anagrafica.citta_residenza = form.cleaned_data["citta_residenza"]
        anagrafica.cap_residenza = form.cleaned_data["cap_residenza"]
        anagrafica.provincia_residenza = form.cleaned_data["provincia_residenza"]

        anagrafica.indirizzo_domicilio = form.cleaned_data["indirizzo_domicilio"]
        anagrafica.citta_domicilio = form.cleaned_data["citta_domicilio"]
        anagrafica.cap_domicilio = form.cleaned_data["cap_domicilio"]
        anagrafica.provincia_domicilio = form.cleaned_data["provincia_domicilio"]

        anagrafica.save()

        recapiti, created = Recapito.objects.get_or_create(recapiti_psicologo=profile)

        recapiti.tel_residenza = form.cleaned_data["tel_residenza"]
        recapiti.tel_domicilio = form.cleaned_data["tel_domicilio"]
        recapiti.tel_ufficio = form.cleaned_data["tel_ufficio"]
        recapiti.tel_cellulare = form.cleaned_data["tel_cellulare"]
        recapiti.indirizzo_email = form.cleaned_data["indirizzo_email"]
        recapiti.indirizzo_pec = form.cleaned_data["indirizzo_pec"]

        recapiti.save()

        if user.email != recapiti.indirizzo_email:
            user.email = recapiti.indirizzo_email
            user.save()

        return super(OOUserProfileEditView, self).form_valid(form)
        

class DocumentGenerator(View):

    # populate these attributes when extending the class
    template_file = None  
    content_type = None
    download_filename = None


    def get_template_file(self, request):
        return self.template_file


    def get_context(self, request):
        return {}


    def replace(self, content, var_name, var_value):

        var_raw_name = "\{\{ %s \}\}" % var_name

        return content.replace(var_raw_name, var_value)



    def generate_document(self, request):
    
        template = self.get_template_file(request)

        if not os.path.exists(template):
            raise ValueError("The specified file '%s' does not exist" % template)

        ctx = self.get_context(request)

        t = open(template, 'r')

        if t:
            content = t.read()

            t.close()

            for var_name, var_value in ctx.items():
                content = self.replace(content, var_name, "%s" % var_value)


            return content

    def get_download_filename(self, request):
    
        template_file = self.get_template_file(request)

        default_name = "document"
    
        if template_file:
            default_name = os.path.basename(template_file)

        return self.download_filename or default_name

    def get(self, request, *args, **kwargs):

        response = HttpResponse(content_type=self.content_type)

        filename = self.get_download_filename(request)
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        content = self.generate_document(request)

        response.write(content)

        return response

class GenerateModuleSezA(DocumentGenerator):

    template_file_man = settings.MODULES["sez_a_uomo"]
    template_file_woman = settings.MODULES["sez_a_donna"]

    def get_template_file(self, request):
        
        person = request.user.get_profile().person

        rel_filename = self.template_file_man

        if person.sex == Person.FEMALE_SEX:
            rel_filename = self.template_file_woman

        return os.path.join(settings.STATIC_ROOT, rel_filename)

    def get_context(self, request):

        profile = request.user.get_profile()

        ctx = {}
        ctx["FIRST_NAME"] = profile.person.first_name
        ctx["LAST_NAME"] = profile.person.last_name
        ctx["BIRTH_LOCATION"] = profile.person.birth_location
        ctx["BIRTH_DATE"] = profile.person.birth_date


        # fields not on DB
        ctx["BIRTH_PROVINCE"] = "_____"
        ctx["CITIZEN"] = "_____"

        try:
            ctx["CF"] = profile.anagrafica.codice_fiscale
            ctx["RESIDENCE_CITY"] = profile.anagrafica.citta_residenza
            ctx["RESIDENCE_PROVINCE"] = profile.anagrafica.provincia_residenza
            ctx["RESIDENCE_ADDRESS"] = profile.anagrafica.indirizzo_residenza
            ctx["RESIDENCE_POSTAL_CODE"] = profile.anagrafica.cap_residenza
        except ObjectDoesNotExist:
            ctx["CF"] = "_____"
            ctx["RESIDENCE_CITY"] = "_____" 
            ctx["RESIDENCE_PROVINCE"] = "______" 
            ctx["RESIDENCE_ADDRESS"] = "_____" 
            ctx["RESIDENCE_POSTAL_CODE"] = "_____"

        try:
            ctx["TELEPHONE"] = profile.recapiti.tel_residenza or profile.recapiti.tel_domicilio
            ctx["MOBILE_PHONE"] = profile.recapiti.tel_cellulare
            ctx["EMAIL"] = profile.recapiti.indirizzo_email or profile.recapiti.indirizzo_pec
        except ObjectDoesNotExist:
            ctx["TELEPHONE"] = "_____"
            ctx["MOBILE_PHONE"] = "_____"
            ctx["EMAIL"] = "_____"

        return ctx

    def get_download_filename(self, request):

        return "modulo_iscrizione_sez_a.rtf"
