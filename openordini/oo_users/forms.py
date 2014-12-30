# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from open_municipio.users.forms import UserRegistrationForm as OMUserRegistrationForm
from open_municipio.people.models import Person

class UserRegistrationForm(OMUserRegistrationForm):

    fieldsets = {
        "access" : ["username", "password", "password1", ],
        "basic" : ["email", "first_name", "last_name", "sex", "birth_date", "birth_location", "uses_nickname", "description", "image", "says_is_psicologo_lavoro", "says_is_psicologo_clinico", "says_is_psicologo_forense", "says_is_asl_employee", "says_is_self_employed", ],
        "contacts": ["indirizzo_residenza", "citta_residenza", "indirizzo_domicilio", "citta_domicilio", "cap", "provincia_domicilio", "codice_fiscale", ],
        "extra" : ["ritiro_agenda", "invio_tesserino"],
    }

    says_is_psicologo_lavoro = forms.BooleanField(required=False, label=_('I am a "psicologo del lavoro"'))
    says_is_psicologo_clinico = forms.BooleanField(required=False, label=_('I am a "psicologo clinico"'))
    says_is_psicologo_forense = forms.BooleanField(required=False, label=_('I am a "psicologo forense"'))

    sex = forms.ChoiceField(choices=Person.SEX, required=True, label=_("Sex"))

    birth_date = forms.DateField(required=True, label=_("Birth date"), widget=forms.widgets.DateInput(format="%d/%m/%Y"), help_text=u"Usa il formato gg/mm/aaaa")
    birth_location = forms.CharField(max_length=100, required=False, label=_("Birth location"))
    register_subscription_date = forms.DateField(required=False, label=_("Register subscription date"), help_text=u"Solo per coloro i quali sono già iscritti all'Albo degli Psicologi. Usa il formato gg/mm/aaaa", widget=forms.widgets.DateInput(format="%d/%m/%Y"))

    is_asl_employee = forms.BooleanField(required=False, label=_('I am an ASL employee'))
    is_self_employed = forms.BooleanField(required=False, label=_('I am self-employed'))

    indirizzo_residenza = forms.CharField(required=True, label=_('Indirizzo residenza'))
    citta_residenza = forms.CharField(required=True, label=_(u'Città residenza'))
    indirizzo_domicilio = forms.CharField(required=True, label=_('Indirizzo domicilio'))
    citta_domicilio = forms.CharField(required=True, label=_(u'Città domicilio'))
    cap = forms.CharField(required=True, label=_('CAP'))
    provincia_domicilio = forms.CharField(required=True, label=_('Provincia domicilio'))
    codice_fiscale = forms.CharField(required=True, label=_('Codice Fiscale'))
    accertamento_casellario = forms.BooleanField(required=False, label=_('Accertamento casellario'))
    accertamento_universita = forms.BooleanField(required=False, label=_('accertamento universita'))

    ritiro_agenda = forms.BooleanField(required=False, label=_('Ritito agenda'))
    invio_tesserino = forms.BooleanField(required=False, label=_('Invio tesserino'))

    class Meta:
        exclude = [ "accertamento_casellario", "accertamento_universita", ]
