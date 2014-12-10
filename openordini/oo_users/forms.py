from django import forms
from django.utils.translation import ugettext_lazy as _

from open_municipio.users.forms import UserRegistrationForm as OMUserRegistrationForm
from open_municipio.people.models import Person

class UserRegistrationForm(OMUserRegistrationForm):
    # TODO handle additional profile fields

    says_is_psicologo_lavoro = forms.BooleanField(required=False, label=_('I am a "psicologo del lavoro"'), help_text=u"Segnala alla redazione che sei uno psicologo del lavoro.")

    says_is_psicologo_clinico = forms.BooleanField(required=False, label=_('I am a "psicologo clinico"'), help_text=u"Segnala alla redazione che sei uno psicologo clinico.")
    says_is_psicologo_forense = forms.BooleanField(required=False, label=_('I am a "psicologo forense"'), help_text=u"Segnala alla redazione che sei uno psicologo forense.")
    sex = forms.ChoiceField(choices=Person.SEX, label=_("Sex"))

    birth_date = forms.DateField(required=True, label=_("Birth date"), widget=forms.widgets.DateInput(format="%d/%m/%Y"), help_text=u"Usa il formato gg/mm/aaaa")
    birth_location = forms.CharField(max_length=100, label=_("Birth location"))

    register_subscription_date = forms.DateField(required=False, label=_("Register subscription date"), widget=forms.widgets.DateInput(format="%d/%m/%Y"), help_text=u"Usa il formato gg/mm/aaaa")
