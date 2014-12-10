from django import forms
from django.utils.translation import ugettext_lazy as _

from open_municipio.users.forms import UserRegistrationForm as OMUserRegistrationForm

class UserRegistrationForm(OMUserRegistrationForm):
    # TODO handle additional profile fields

    says_is_psicologo_lavoro = forms.BooleanField(required=False, label=_('I am a "psicologo del lavoro"'), help_text=u"Segnala alla redazione che sei uno psicologo del lavoro.")

    says_is_psicologo_clinico = forms.BooleanField(required=False, label=_('I am a "psicologo clinico"'), help_text=u"Segnala alla redazione che sei uno psicologo clinico.")
    says_is_psicologo_forense = forms.BooleanField(required=False, label=_('I am a "psicologo forense"'), help_text=u"Segnala alla redazione che sei uno psicologo forense.")
