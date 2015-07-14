# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.db import transaction
from django.contrib.auth import login, get_backends
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_text
from open_municipio.locations.models import Location

#from open_municipio.users.forms import UserRegistrationForm
from open_municipio.users.models import UserProfile as OMUserProfile
from open_municipio.people.models import Person, Institution, InstitutionCharge
from .forms import UserRegistrationForm
from .models import UserProfile, Recapito, ExtraPeople

from registration.signals import user_registered
from registration.signals import user_activated
from django.dispatch import receiver

from django.db.models import Q


"""
Functions listed below act as receivers and are used along the
registration workflow.
"""

logger = logging.getLogger("registration")

def format_data(data):
    log_data = "\n    ".join(map(lambda k: "%s : %s" % (k, data[k]) if "password" not in k else ("%s : xxx" % k), data.keys()))
    return "    %s" % log_data



@transaction.commit_on_success
@receiver(user_registered)
def user_created(sender, user, request, **kwargs):
    """
    As soon as a new ``User`` is created, the correspondent
    ``UserProfile`` must be created too. Necessary information is
    supposed to be found in POST data.
    """
    r = self.request
    # print "salva utente: %s (user = %s)..." % (user_registered, user)
    # deletes the user profiles created by OM ... it's not
    # very efficient (INSERT + DELETE) but makes the two systems
    # more decoupled
    OMUserProfile.objects.filter(user=user).delete()

    form = UserRegistrationForm(request.POST)

    # this is required to populate form.cleaned_data used in the following
    form.is_valid()

    # create the user
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']

    # format data for error message (if needed)
    log_data = format_data(form.data)

    try:
        user.save()
        msg = _(u"A new user registered on the website: %(user)s") % { "user":smart_text(user) }
        logger.info(msg)
    except Exception, e:
        subject = _(u"It was not possible to register user: %(user)s") % { "user":smart_text(user) }

        msg = _("%(subject)s.\n\nDetails: %(error)s\n\nProvided data:\n\n%(data)s") % { "subject": subject, "error": smart_text(e), "data": smart_text(log_data) }

        d = { "subject": subject }

        logger.warning(msg, extra=d)

        # do not continue with registration, in this case
        return

        
    # create the userprofile

    says_is_psicologo_clinico = form.cleaned_data.get('says_is_psicologo_clinico', False)
    says_is_psicologo_lavoro = form.cleaned_data.get('says_is_psicologo_lavoro', False)
    says_is_psicologo_forense = form.cleaned_data.get('says_is_psicologo_forense', False)
    says_is_dottore_tecniche_psicologiche = form.cleaned_data.get('says_is_dottore_tecniche_psicologiche', False)

    register_subscription_date = form.cleaned_data.get('register_subscription_date', False)

    extra_data = UserProfile(user=user)
    extra_data.says_is_politician = False 
    extra_data.says_is_psicologo_clinico = says_is_psicologo_clinico
    extra_data.says_is_psicologo_lavoro = says_is_psicologo_lavoro
    extra_data.says_is_psicologo_forense = says_is_psicologo_forense
    extra_data.says_is_dottore_tecniche_psicologiche = says_is_dottore_tecniche_psicologiche
    extra_data.is_asl_employee = form.cleaned_data.get('is_asl_employee', False)
    extra_data.is_self_employed = form.cleaned_data.get('is_self_employed', False)
    extra_data.uses_nickname = form.cleaned_data.get('uses_nickname', False)
    extra_data.wants_newsletter = form.data.get('wants_newsletter', False)
    extra_data.location = Location.objects.get(pk=form.data['location']) if ("location" in form.data) and (form.data['location'] != '') else None
    extra_data.description = form.cleaned_data['description']
    extra_data.codice_fiscale  = form.cleaned_data.get('codice_fiscale',False)
#    extra_data.image =  person.img
#    extra_data.person = person
    extra_data.register_subscription_date = register_subscription_date

    try:
        extra_data.save()
    except Exception, e:
        subject =_(u"It was not possible to register user: %(user)s") % { "user":smart_text(user) }

        msg = _("%(subject)s.\n\nDetails: %(error)s\n\nProvided data:\n\n%(data)s") % { "subject": subject, "error": smart_text(e), "data": smart_text(log_data) }

        d = { "subject": subject }


        logger.warning(msg, extra=d)
        # continue even in case of error

    # create the person

    person = Person()
    person.first_name = user.first_name
    person.last_name = user.last_name
    person.birth_date = form.cleaned_data["birth_date"]
    person.birth_location = form.cleaned_data.get("birth_location", None)
    person.sex = form.cleaned_data["sex"]
    person.img = request.FILES.get('image', None)

    try:
        person.save()

        # link the extra_data object to the person
        extra_data.person = person
        extra_data.image = person.img
        extra_data.save()

    except Exception, e:
        subject = _(u"It was not possible to save the personal data of user: %(user)s") % { "user": smart_text(user) }

        msg = _("%(subject)s.\n\nDetails: %(error)s\n\nProvided data:\n\n%(data)s") % { "subject": subject, "error": smart_text(e), "data": smart_text(log_data) }

        d = { "subject": subject }

        logger.warning(msg, extra=d)

        # do not continue, in case the person was not saved
        return 


    # aggiungi recapiti
    extra_data_recapiti = ExtraPeople(anagrafica_extra=extra_data)
    extra_data_recapiti.indirizzo_residenza = form.cleaned_data.get('indirizzo_residenza',False)
    extra_data_recapiti.citta_residenza  = form.cleaned_data.get('citta_residenza',False)
    extra_data_recapiti.cap_residenza  = form.cleaned_data.get('cap_residenza',False)
    extra_data_recapiti.provincia_residenza  = form.cleaned_data.get('provincia_residenza',False)
    extra_data_recapiti.indirizzo_domicilio = form.cleaned_data.get('indirizzo_domicilio',False)
    extra_data_recapiti.citta_domicilio  = form.cleaned_data.get('citta_domicilio',False)
    extra_data_recapiti.cap_domicilio  = form.cleaned_data.get('cap_domicilio',False)
    extra_data_recapiti.provincia_domicilio  = form.cleaned_data.get('provincia_domicilio',False)    
    extra_data_recapiti.indirizzo_studio = form.cleaned_data.get('indirizzo_studio',False)
    extra_data_recapiti.citta_studio  = form.cleaned_data.get('citta_studio',False)
    extra_data_recapiti.cap_studio  = form.cleaned_data.get('cap_studio',False)
    extra_data_recapiti.provincia_studio  = form.cleaned_data.get('provincia_studio',False)    
    extra_data_recapiti.save()


    # aggiungi a gruppi e commissioni

def finalize_registration(self, user): 
    print("sono dentro FINALIZE_REGISTRATION, prima del check di 'numero_iscrizione'")
    print user.numero_iscrizione
    if settings.REGISTRATION_AUTO_ADD_GROUP and user.numero_iscrizione: 
        is_registered_a = (user.register_subscription_date != None) and (user.says_is_psicologo_lavoro or user.says_is_psicologo_clinico or user.says_is_psicologo_forense or user.says_is_self_employed)
        if is_registered_a:
        	print "test 1 - inserisco in albo -> is_registered_a"
        	i = Institution.objects.get(slug="sezione-a")             	
        	if InstitutionCharge.objects.filter(person__pk=user.person.id).filter(institution=i).count()  == 0:        		
        	   	member_charge = InstitutionCharge(person=user.person, institution=i, start_date=user.register_subscription_date) 
   	   	       	member_charge.save()

        if user.says_is_psicologo_lavoro:
            g, created = Group.objects.get_or_create(name=settings.SYSTEM_GROUP_NAMES["psicologo_lavoro"])
            g.user_set.add(user.user)
        if user.says_is_psicologo_clinico:
            g, created = Group.objects.get_or_create(name=settings.SYSTEM_GROUP_NAMES["psicologo_clinico"])
            g.user_set.add(user.user)
        if user.says_is_psicologo_forense:
            g, created = Group.objects.get_or_create(name=settings.SYSTEM_GROUP_NAMES["psicologo_forense"])
            g.user_set.add(user.user)
        if user.says_is_self_employed:
            g, created = Group.objects.get_or_create(name=settings.SYSTEM_GROUP_NAMES["psicologo"])
            l = user.user.groups.values_list('name',flat=True)
            print "l'utente appartene ad un gruppo: %s" % (l)
            #g.user_set.add(user.user)
            check_group_user_exist(g,user)
            

        is_registered_b = (user.register_subscription_date != None) and (user.says_is_dottore_tecniche_psicologiche)
        if is_registered_b: # TODO: check the indentation for this IF
            print "test 1 - inserisco in albo -> is_registered_b"
            i = Institution.objects.get(slug="sezione-b")
            print "denominazione istituzione" % (d)
            if InstitutionCharge.objects.filter(person__pk=user.person.id).filter(institution=i).count()  == 0: 
        	   	member_charge = InstitutionCharge(person=user.person, institution=i, start_date=user.register_subscription_date) 
        	   	member_charge.save() 


        if user.says_is_dottore_tecniche_psicologiche:
            g, created = Group.objects.get_or_create(name=settings.SYSTEM_GROUP_NAMES["dottore_tecniche_psicologiche"])
            g.user_set.add(user.user)
       
       	            
        print('registrazione avvenuta')

def check_group_user_exist(g, u):
   	print "test accesso alla funzione"
   	if User.objects.filter(pk=u.user.id).exists():
   		print "test esiste l'utente, in realtà check inutile perchè veniamo dalla modifica"
   		if Group.objects.filter(pk=g.id):
   			print "test esistenza del gruppo, qui il gruppo esiste sempre, perche o creato o selezionato"
   			if not u.user.groups.exists(): # verifica inutile mi serve sapere il gruppo specifico
   				print "ultima fase, quella necessaria, ossia, l utente ha gia' il suo gruppo"
   				g.user_set.add(u.user)
      

@receiver(user_activated)
def log_in_user(sender, user, request, **kwargs):
    """
    Dirty trick to let the user automatically logged-in at the end of
    the registration process.
    """
    if getattr(settings, 'REGISTRATION_AUTO_LOGIN', False):
        backend = get_backends()[0] # A bit of a hack to bypass `authenticate()`.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        login(request, user)
