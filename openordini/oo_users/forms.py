# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from open_municipio.users.forms import UserRegistrationForm as OMUserRegistrationForm
from open_municipio.people.models import Person

class UserRegistrationForm(OMUserRegistrationForm):

    says_is_psicologo_lavoro = forms.BooleanField(required=False, label=_('I am a "psicologo del lavoro"'))
    says_is_psicologo_clinico = forms.BooleanField(required=False, label=_('I am a "psicologo clinico"'))
    says_is_psicologo_forense = forms.BooleanField(required=False, label=_('I am a "psicologo forense"'))

    sex = forms.ChoiceField(choices=Person.SEX, required=True, label=_("Sex"))

    birth_date = forms.DateField(required=True, label=_("Birth date"), widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    birth_location = forms.CharField(max_length=100, required=False, label=_("Birth location"))
    register_subscription_date = forms.DateField(required=False, label=_("Register subscription date"), help_text=u"Solo per gli utenti che sono già iscritti all'Albo degli Psicologi", widget=forms.widgets.DateInput(format="%d/%m/%Y"))

    is_asl_employee = forms.BooleanField(required=False, label=_('I am an ASL employee'))
    is_self_employed = forms.BooleanField(required=False, label=_('I am self-employed'))

