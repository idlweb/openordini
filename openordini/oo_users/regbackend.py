from django.conf import settings
from django.db import transaction
from django.contrib.auth import login, get_backends
from django.contrib.auth.models import Group
from open_municipio.locations.models import Location

#from open_municipio.users.forms import UserRegistrationForm
from open_municipio.users.models import UserProfile as OMUserProfile
from open_municipio.people.models import Person, Institution, InstitutionCharge
from .forms import UserRegistrationForm
from .models import UserProfile, Recapito

from registration.signals import user_registered
from registration.signals import user_activated
from django.dispatch import receiver

"""
Functions listed below act as receivers and are used along the
registration workflow.
"""


@transaction.commit_on_success
@receiver(user_registered)
def user_created(sender, user, request, **kwargs):
    """
    As soon as a new ``User`` is created, the correspondent
    ``UserProfile`` must be created too. Necessary information is
    supposed to be found in POST data.
    """

    print "salva utente: %s (user = %s)..." % (user_registered, user)
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
    user.save()

    # create the person

    person = Person()
    person.first_name = user.first_name
    person.last_name = user.last_name
    person.birth_date = form.cleaned_data["birth_date"]
    person.birth_location = form.cleaned_data.get("birth_location", None)
    person.sex = form.cleaned_data["sex"]
    person.img = request.FILES.get('image', None)
    person.save()

    # create the userprofile

    says_is_psicologo_clinico = form.cleaned_data.get('says_is_psicologo_clinico', False)
    says_is_psicologo_lavoro = form.cleaned_data.get('says_is_psicologo_lavoro', False)
    says_is_psicologo_forense = form.cleaned_data.get('says_is_psicologo_forense', False)

    register_subscription_date = form.cleaned_data.get('register_subscription_date', False)

    extra_data = UserProfile(user=user)
    extra_data.says_is_politician = False 
    extra_data.says_is_psicologo_clinico = says_is_psicologo_clinico
    extra_data.says_is_psicologo_lavoro = says_is_psicologo_lavoro
    extra_data.says_is_psicologo_forense = says_is_psicologo_forense
    extra_data.is_asl_employee = form.cleaned_data.get('is_asl_employee', False)
    extra_data.is_self_employed = form.cleaned_data.get('is_self_employed', False)
    extra_data.uses_nickname = form.cleaned_data.get('uses_nickname', False)
    extra_data.wants_newsletter = form.data.get('wants_newsletter', False)
    extra_data.location = Location.objects.get(pk=form.data['location']) if ("location" in form.data) and (form.data['location'] != '') else None
    extra_data.description = form.cleaned_data['description']
    extra_data.image =  person.img
    extra_data.person = person
    extra_data.register_subscription_date = register_subscription_date
    extra_data.save()

    # aggiungi recapiti
    extra_data_recapiti = Recapito(recapiti_psicologo=extra_data)
    extra_data_recapiti.indirizzo_residenza = form.cleaned_data.get('indirizzo_residenza',False)
    extra_data_recapiti.save()
    # aggiungi a gruppi e commissioni

    if settings.REGISTRATION_AUTO_ADD_GROUP:

        is_registered = (register_subscription_date != None)

        if says_is_psicologo_lavoro:

            g,created = Group.objects.get_or_create(name=settings.SYSTEM_GROUP_NAMES["psicologo_lavoro"])
            g.user_set.add(user)

            if is_registered:
                i = Institution.objects.get(slug=settings.COMMITTEE_SLUGS["psicologo_lavoro"])

                member_charge = InstitutionCharge(person=person, institution=i, start_date=register_subscription_date)
                member_charge.save()
 
        if says_is_psicologo_clinico:
            g,created = Group.objects.get_or_create(name=settings.SYSTEM_GROUP_NAMES["psicologo_clinico"])
            g.user_set.add(user)

            if is_registered: 
                i = Institution.objects.get(slug=settings.COMMITTEE_SLUGS["psicologo_clinico"])

                member_charge = InstitutionCharge(person=person, institution=i, start_date=register_subscription_date)
                member_charge.save()


    
        if says_is_psicologo_forense:
            g,created = Group.objects.get_or_create(name=settings.SYSTEM_GROUP_NAMES["psicologo_forense"])

            g.user_set.add(user)
    
            if is_registered: 
                i = Institution.objects.get(slug=settings.COMMITTEE_SLUGS["psicologo_forense"])
                member_charge = InstitutionCharge(person=person, institution=i, start_date=register_subscription_date)
                member_charge.save()



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
