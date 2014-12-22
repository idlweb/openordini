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

    birth_date = forms.DateField(required=True, label=_("Birth date"), widget=forms.widgets.DateInput(format="%d/%m/%Y"), help_text=u"Usa il formato gg/mm/aaaa")
    birth_location = forms.CharField(max_length=100, required=False, label=_("Birth location"))
    register_subscription_date = forms.DateField(required=False, label=_("Register subscription date"), help_text=u"Solo per coloro i quali sono già iscritti all'Albo degli Psicologi. Usa il formato gg/mm/aaaa", widget=forms.widgets.DateInput(format="%d/%m/%Y"))

    is_asl_employee = forms.BooleanField(required=False, label=_('I am an ASL employee'))
    is_self_employed = forms.BooleanField(required=False, label=_('I am self-employed'))

    indirizzo_residenza = forms.CharField(required=True, label=_('indirizzo di residenza'))
    citta_residenza = forms.CharField(required=True, label=_('citta di residenza'))
    indirizzo_domicilio = forms.CharField(required=True, label=_('indirizzo domicilio'))
    citta_domicilio = forms.CharField(required=True, label=_('citta domicilio'))
    cap = forms.CharField(required=True, label=_('CAP'))
    provincia_domicilio = forms.CharField(required=True, label=_('provincia domicilio'))
    codice_fiscale = forms.CharField(required=True, label=_('codice fiscale'))
    accertamento_casellario = forms.BooleanField(required=True, label=_('accertamento casellario'))
    accertamento_universita = forms.BooleanField(required=True, label=_('accertamento universita'))

    ritiro_agenda = forms.CharField(required=False, label=_('ritito_agenda'))
    invio_tesserino = forms.CharField(required=False, label=_('invio_tesserino'))


