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
from openordini.mvdb.models import Regioni, Provincie, Comuni

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
        ctx["acts_fascicoli"] = None

        try:
            curr_person = self.object.person

#            print "person: %s" % curr_person
            ctx["acts_fascicoli"]  = Fascicolo.objects.filter(recipient_set__person=curr_person).distinct()

            curr_year = datetime.today().year

            ctx["curr_subscription"] = None

            if curr_person:
                ctx["curr_subscription"] = SubscriptionOrder.get_for_person(curr_person, curr_year)

        except (ObjectDoesNotExist, AttributeError), err:
            print "error: %s" % err


        """ 
        map: data una funzione ed una sequenza 
        applica quella funzione ad ogni elemento
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
        print "catched here ..."
        initial = super(OOUserProfileEditView, self).get_initial()

        user = self.request.user

        profile = user.get_profile()


        initial["location"] = profile.location
        initial["description"] = profile.description
        initial["image"] = profile.image
        initial["uses_nickname"] = profile.uses_nickname
        initial["username"] = user.username 
        
        def region_from_provincia(provincia="Bari"):
            #provincia_istat = tuple(Provincie.objects.filter(name=provincia).values_list())
            #regione = tuple(Regioni.objects.filter(codice_regione_istat=provincia_istat[0][5]).values_list())
            provincia_istat = Provincie.objects.get(name=provincia).codice_regione_istat                            
            regione = Regioni.objects.get(codice_regione_istat=provincia_istat).name
            return regione#.name#[0][1]

        try:            
            initial["regione_residenza"] =  region_from_provincia(profile.anagrafica.provincia_residenza)
            initial["indirizzo_residenza"] = profile.anagrafica.indirizzo_residenza
            initial["citta_residenza"] = profile.anagrafica.citta_residenza
            initial["cap_residenza"] = profile.anagrafica.cap_residenza
            initial["provincia_residenza"] = profile.anagrafica.provincia_residenza

            initial["regione_domicilio"] =  region_from_provincia(profile.anagrafica.provincia_domicilio)            
            initial["indirizzo_domicilio"] = profile.anagrafica.indirizzo_domicilio
            initial["citta_domicilio"] = profile.anagrafica.citta_domicilio
            initial["cap_domicilio"] = profile.anagrafica.cap_domicilio
            initial["provincia_domicilio"] = profile.anagrafica.provincia_domicilio

            initial["regione_studio"] =  region_from_provincia(profile.anagrafica.provincia_studio)
            initial["indirizzo_studio"] = profile.anagrafica.indirizzo_studio
            initial["citta_studio"] = profile.anagrafica.citta_studio
            initial["cap_studio"] = profile.anagrafica.cap_studio
            initial["provincia_studio"] = profile.anagrafica.provincia_studio
            initial["denominazione_studio"] = profile.anagrafica.denominazione_studio
            initial["coord_lat"] = profile.anagrafica.coord_lat
            initial["coord_long"] = profile.anagrafica.coord_long

        except ObjectDoesNotExist:
            pass


        try:
            initial["first_name"] = user.first_name
            initial["last_name"] = user.last_name
            initial["email"] = user.email
            initial["birth_date"] = user.get_profile().person.birth_date
            initial["birth_location"] = user.get_profile().person.birth_location
            initial["sex"] = user.get_profile().person.sex                
        except ObjectDoesNotExist:
            pass
     

        try:
            initial["says_is_psicologo_lavoro"] = profile.says_is_psicologo_lavoro
            initial["says_is_psicologo_clinico"] = profile.says_is_psicologo_clinico
            initial["says_is_psicologo_forense"] = profile.says_is_psicologo_forense
            initial["says_is_dottore_tecniche_psicologiche"] = profile.says_is_dottore_tecniche_psicologiche 
            initial["is_asl_employee"] = profile.says_is_asl_employee
            initial["is_self_employed"] = profile.says_is_self_employed
            initial["register_subscription_date"] = profile.register_subscription_date
            initial["wants_newsletter"] = profile.wants_newsletter
            initial["wants_commercial_newsletter"] = profile.wants_commercial_newsletter
            initial["wants_commercial_mobile"] = profile.wants_commercial_mobile            
        except ObjectDoesNotExist:
            pass
      

        try:
            initial["tel_residenza"] = profile.recapiti.tel_residenza
            initial["tel_domicilio"] = profile.recapiti.tel_domicilio
            initial["tel_ufficio"] = profile.recapiti.tel_ufficio
            initial["tel_cellulare"] = profile.recapiti.tel_cellulare
            initial["indirizzo_email"] = profile.recapiti.indirizzo_email #or profile.user.emaliil
            initial["indirizzo_pec"] = profile.recapiti.indirizzo_pec
            initial["sito_internet"] = profile.recapiti.sito_internet
            initial["consegna_corrispondenza"] = profile.recapiti.consegna_corrispondenza
        except ObjectDoesNotExist:
            pass

        return initial
    
    def form_invalid(self, form):
        print "form errors: %s" % form.errors        
        return super(OOUserProfileEditView, self).form_invalid(form)


    def form_valid(self, form):

        #print "form valid ..."
        #print "data: %s" % form.cleaned_data
        #save data
        #print "per capire il form %s" % (form.__dict__)        
        #print "per capire %s" % (UserProfileForm.__name___) 
        user = self.request.user
        #print "l utente - %s" % (user)

        pwd = form.cleaned_data["password1"]

        #print "questa e' la pwd %s" %(pwd)
        try:
            #print "eseguo..."
            user.username = form.cleaned_data["username"] or user.username
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"] or "info@info.it"
            user.set_password(pwd)
            user.save()
            #print "pwd settata"
            #pass
        except Exception, e:
            print "errore %s" % (e)
            #raise
        

        profile = user.get_profile()
        profile.location = form.cleaned_data["location"]
        profile.description = form.cleaned_data["description"]
        profile.image = form.cleaned_data["image"]
        profile.uses_nickname = form.cleaned_data["uses_nickname"]
        profile.says_is_psicologo_lavoro = form.cleaned_data["says_is_psicologo_lavoro"]
        profile.says_is_psicologo_clinico = form.cleaned_data["says_is_psicologo_clinico"]
        profile.says_is_psicologo_forense = form.cleaned_data["says_is_psicologo_forense"]
        profile.says_is_dottore_tecniche_psicologiche = form.cleaned_data["says_is_dottore_tecniche_psicologiche"]

        #profile.says_is_asl_employee = form.cleaned_data["says_is_asl_employee"] or 0
        #profile.says_is_self_employed = form.cleaned_data["says_is_self_employed"] or 0

        profile.register_subscription_date = form.cleaned_data["register_subscription_date"]
        profile.wants_newsletter = form.cleaned_data["wants_newsletter"]
        profile.wants_commercial_newsletter = form.cleaned_data["wants_commercial_newsletter"]
        profile.wants_commercial_mobile = form.cleaned_data["wants_commercial_mobile"]
        profile.save()

        person = user.get_profile().person
        person.birth_date = form.cleaned_data["birth_date"]
        person.birth_location = form.cleaned_data["birth_location"]
        person.sex = form.cleaned_data["sex"]
        person.save()

        anagrafica, created = ExtraPeople.objects.get_or_create(anagrafica_extra=profile)
        anagrafica.indirizzo_residenza = form.cleaned_data["indirizzo_residenza"]
        anagrafica.citta_residenza = form.cleaned_data["citta_residenza"]
        anagrafica.cap_residenza = form.cleaned_data["cap_residenza"]
        anagrafica.provincia_residenza = form.cleaned_data["provincia_residenza"]
        anagrafica.indirizzo_domicilio = form.cleaned_data["indirizzo_domicilio"]
        anagrafica.citta_domicilio = form.cleaned_data["citta_domicilio"]
        anagrafica.cap_domicilio = form.cleaned_data["cap_domicilio"]
        anagrafica.provincia_domicilio = form.cleaned_data["provincia_domicilio"]
        anagrafica.indirizzo_studio = form.cleaned_data["indirizzo_studio"]
        anagrafica.citta_studio = form.cleaned_data["citta_studio"]
        anagrafica.cap_studio = form.cleaned_data["cap_studio"]
        anagrafica.provincia_studio = form.cleaned_data["provincia_studio"]
        anagrafica.denominazione_studio = form.cleaned_data["denominazione_studio"]
        anagrafica.coord_lat = form.cleaned_data["coord_lat"]
        anagrafica.coord_long = form.cleaned_data["coord_long"]
        anagrafica.save()

        recapiti, created = Recapito.objects.get_or_create(recapiti_psicologo=profile)
        recapiti.tel_residenza = form.cleaned_data["tel_residenza"]
        recapiti.tel_domicilio = form.cleaned_data["tel_domicilio"]
        recapiti.tel_ufficio = form.cleaned_data["tel_ufficio"]
        recapiti.tel_cellulare = form.cleaned_data["tel_cellulare"]
        recapiti.indirizzo_email = form.cleaned_data["indirizzo_email"]
        recapiti.indirizzo_pec = form.cleaned_data["indirizzo_pec"]
        recapiti.sito_internet = form.cleaned_data["sito_internet"]
        recapiti.consegna_corrispondenza = form.cleaned_data["consegna_corrispondenza"]
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
