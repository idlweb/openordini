from django.conf import settings
from django.contrib.auth import login, get_backends
from django.contrib.auth.models import Group
from open_municipio.locations.models import Location

#from open_municipio.users.forms import UserRegistrationForm
from open_municipio.users.models import UserProfile as OMUserProfile
from open_municipio.people.models import Person
from .forms import UserRegistrationForm
from .models import UserProfile

from registration.signals import user_registered
from registration.signals import user_activated
from django.dispatch import receiver

"""
Functions listed below act as receivers and are used along the
registration workflow.
"""


@receiver(user_registered)
def user_created(sender, user, request, **kwargs):
    """
    As soon as a new ``User`` is created, the correspondent
    ``UserProfile`` must be created too. Necessary information is
    supposed to be found in POST data.
    """

    # deletes the user profiles created by OM ... it's not
    # very efficient (INSERT + DELETE) but makes the two systems
    # more decoupled
    OMUserProfile.objects.filter(user=user).delete()


    form = UserRegistrationForm(request.POST)

    # this populates the form.cleaned_data dict
    form.is_valid()

    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    user.save()

    # create the Person
    person  = Person()
    person.first_name = form.cleaned_data['first_name']
    person.last_name = form.cleaned_data['last_name']
    person.img =  request.FILES.get('image', None)
    person.birth_date = form.cleaned_data.get('birth_date', None)
    person.birth_location = form.cleaned_data.get('birth_location', None)
    person.sex = form.cleaned_data['sex']
    person.save()
 
    # create the UserProfile

    is_psi_forense = form.cleaned_data.get('says_is_psicologo_forense', False)
    is_psi_lavoro = form.cleaned_data.get('says_is_psicologo_lavoro', False)    
    is_psi_clinico = form.cleaned_data.get('says_is_psicologo_clinico', False)   


    extra_data = UserProfile(user=user)
    extra_data.says_is_politician = False # we don't handle politicians here ;)
    extra_data.says_is_psicologo_clinico = is_psi_clinico
    extra_data.says_is_psicologo_lavoro = is_psi_lavoro
    extra_data.says_is_psicologo_forense = is_psi_forense

    extra_data.uses_nickname = form.data['uses_nickname'] if 'uses_nickname' in form.data else False
    extra_data.wants_newsletter = False
    extra_data.wants_newsletter = form.data['wants_newsletter'] if 'wants_newsletter' in form.data else False
    extra_data.location = Location.objects.get(pk=form.data['location']) if ("location" in form.data) and (form.data['location'] != '') else None
    extra_data.description = form.data['description']
    extra_data.image = request.FILES['image'] if 'image' in request.FILES else None
    extra_data.person = person
    extra_data.save()

    # add the user to his/her groups
    if settings.REGISTRATION_GROUP_MEMBERS_AUTO:
        if is_psi_clinico:
            g,created = Group.objects.get_or_create(name=settings.GROUP_PSICOLOGO_CLINICO)
            g.user_set.add(user)

        if is_psi_forense:
            g,created = Group.objects.get_or_create(name=settings.GROUP_PSICOLOGO_FORENSE)
            g.user_set.add(user)

        if is_psi_lavoro:
            g,created = Group.objects.get_or_create(name=settings.GROUP_PSICOLOGO_LAVORO)
            g.user_set.add(user)
       


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
