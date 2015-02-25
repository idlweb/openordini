# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from open_municipio.users.forms import UserRegistrationForm as OMUserRegistrationForm, UserProfileForm as OMUserProfileForm
from open_municipio.people.models import Person
from open_municipio.locations.models import Location

from openordini.commons.widgets import ChainedSelect
from openordini.oo_users.models import Recapito
from openordini.mvdb.models import Regioni, Provincie, Comuni
from localflavor.it.forms import ITSocialSecurityNumberField, ITRegionProvinceSelect
from openordini.mvdb.models import Comuni

_cached_values = False

regioni = None
provincie = None
comuni = None

CHOICES_REGIONI = []
CHOICES_PROVINCIE = []
CHOICES_COMUNI = []

provincie_regioni = {}
comuni_provincie = {}

def populate_geo_cache(*args, **kwargs):
    """
    Encapsulate geo queries in this method. In this way, geo-models are not
    loaded before the syncdb can happen (causing exceptions at deploy time
    on new installations)
    """
    global _cached_values

    if _cached_values == True:
        return

    regioni = Regioni.objects.all().order_by("name")
    provincie = Provincie.objects.all().order_by("name")
    comuni = Comuni.objects.all().order_by("name")

    CHOICES_REGIONI = [ ("","---") ]
    if regioni.count() > 0:
        CHOICES_REGIONI += map(lambda r: (r.name, r.name), regioni)

    CHOICES_PROVINCIE = [ ("","---") ]
    if provincie.count() > 0:
        CHOICES_PROVINCIE += map(lambda p: (p.name, p.name), provincie)

    CHOICES_COMUNI = [ ("","---") ]
    if comuni.count() > 0:
        CHOICES_COMUNI += map(lambda c: (c.name, c.name), comuni)


    dict_regioni = {}
    for r in regioni:
        dict_regioni[r.codice_regione_istat] = r.name

    dict_provincie = {}
    provincie_regioni = {}
    for p in provincie:
        id_regione = dict_regioni.get(p.codice_regione_istat, None)
        dict_provincie[p.codice_provincia_istat] = p.name

        if id_regione:
            provincie_regioni[p.name] = id_regione
        else:
            print "regione not found: %s" % p.codice_regione_istat

    comuni_provincie = {}
    for c in comuni:
        id_provincia = dict_provincie[c.codice_provincia_istat]
    
        if id_provincia:
            comuni_provincie[c.name] = id_provincia
        else:
            print "provincia not found: %s" % c.codice_provincia_istat

    #print "collegamento: %s" % provincie_regioni
    #print "comuni: %s; choices: %s" % (comuni, CHOICES_COMUNI)
    #print "regioni = %s, choices = %s" % (regioni, CHOICES_REGIONI)

    _cached_values = True

if not _cached_values:
    # populate the cache of Regioni, Provincie and Comuni, the first time
    populate_geo_cache()

class UserRegistrationForm(OMUserRegistrationForm):

    fieldsets = {
        "access" : ["username", "password", "password1", ],
        "basic" : ["email", "first_name", "last_name", "sex", "birth_date", "birth_location", "uses_nickname", "description", "image", "says_is_psicologo_lavoro", "says_is_psicologo_clinico", "says_is_psicologo_forense", "says_is_asl_employee", "says_is_self_employed", ],
        "contacts": ["indirizzo_residenza", "citta_residenza", "cap_residenza", "regione_residenza", "provincia_residenza", "indirizzo_domicilio", "citta_domicilio", "cap_domicilio", "regione_domicilio", "provincia_domicilio", "indirizzo_studioo", "citta_studio", "cap_studio", "regione_studio", "provincia_studio", "codice_fiscale", ],
        "extra" : ["ritiro_agenda", "invio_tesserino"],
        "note" : ["note_legali"],
    }

    says_is_psicologo_lavoro = forms.BooleanField(required=False, label=_('I am a "psicologo del lavoro"'))
    says_is_psicologo_clinico = forms.BooleanField(required=False, label=_('I am a "psicologo clinico"'))
    says_is_psicologo_forense = forms.BooleanField(required=False, label=_('I am a "psicologo forense"'))
    says_is_dottore_tecniche_psicologiche = forms.BooleanField(required=False, label=_('I am a "dottore in tecniche psicologiche"'))

    wants_commercial_newsletter = forms.BooleanField(required=False, label=_("Autorizzo l'uso della mia casella di posta elettronica"))
    wants_commercial_mobile = forms.BooleanField(required=False, label=_("Consento utilizzo numero cellulare"))

    sex = forms.ChoiceField(choices=Person.SEX, required=True, label=_("Sex"))

    birth_date = forms.DateField(required=True, label=_("Birth date"), widget=forms.widgets.DateInput(format="%d/%m/%Y", attrs=
                                {
                                    'class':'datepicker'
                                }), help_text=u"Usa il formato gg/mm/aaaa")
    birth_location = forms.CharField(max_length=100, required=False, label=_("Birth location"))
    register_subscription_date = forms.DateField(required=False, label=_("Register subscription date"), help_text=u"Solo per coloro i quali sono già iscritti all'Albo degli Psicologi. Usa il formato gg/mm/aaaa", widget=forms.widgets.DateInput(format="%d/%m/%Y", attrs=
                                {
                                    'class':'datepicker'
                                }))

    is_asl_employee = forms.BooleanField(required=False, label=_('I am an ASL employee'))
    is_self_employed = forms.BooleanField(required=False, label=_('I am self-employed'))

    indirizzo_residenza = forms.CharField(required=True, label=_('Indirizzo'))
#    provincia_residenza = forms.CharField(required=True, label=_('Provincia'))
#    citta_residenza = forms.CharField(required=True, label=_(u'Città'))
    regione_residenza = forms.ChoiceField(choices=CHOICES_REGIONI, required=True, label=_('Regione'), initial=settings.REGISTRATION_DEFAULT_REGIONE)
    provincia_residenza = forms.ChoiceField(choices=CHOICES_PROVINCIE, required=True, label=_('Provincia'), widget=ChainedSelect(chained_values=provincie_regioni))
    citta_residenza = forms.ChoiceField(choices=CHOICES_COMUNI, required=True, widget=ChainedSelect(chained_values=comuni_provincie), label=_(u'Città'))
    cap_residenza = forms.CharField(required=True, label=_('CAP'))


    indirizzo_domicilio = forms.CharField(required=True, label=_('Indirizzo'))
    regione_domicilio = forms.ChoiceField(choices=CHOICES_REGIONI, required=True, label=_('Regione'), initial=settings.REGISTRATION_DEFAULT_REGIONE)
#    provincia_domicilio = forms.CharField(required=True, label=_('Provincia'))
#    citta_domicilio = forms.CharField(required=True, label=_(u'Città'))
    provincia_domicilio = forms.ChoiceField(choices=CHOICES_PROVINCIE, required=True, label=_('Provincia'), widget=ChainedSelect(chained_values=provincie_regioni))
    citta_domicilio = forms.ChoiceField(choices=CHOICES_COMUNI, required=True, label=_(u'Città'), widget=ChainedSelect(chained_values=comuni_provincie))
    cap_domicilio = forms.CharField(required=True, label=_('CAP'))

    
    indirizzo_studio = forms.CharField(required=True, label=_('Indirizzo'))
    regione_studio = forms.ChoiceField(choices=CHOICES_REGIONI, required=True, label=_('Regione'), initial=settings.REGISTRATION_DEFAULT_REGIONE)
#    provincia_studio = forms.CharField(required=True, label=_('Provincia'))
#    citta_studio = forms.CharField(required=True, label=_(u'Città'))
    provincia_studio = forms.ChoiceField(choices=CHOICES_PROVINCIE, required=True, label=_('Provincia'), widget=ChainedSelect(chained_values=provincie_regioni))
    citta_studio = forms.ChoiceField(choices=CHOICES_COMUNI, required=True, label=_(u'Città'), widget=ChainedSelect(chained_values=comuni_provincie))

    cap_studio = forms.CharField(required=True, label=_('CAP'))


    consegna_corrispondenza = forms.ChoiceField(choices=Recapito.TIPI_CORRISPONDENZA , required=True, label=_('consegna corrispondenza'))

    #codice_fiscale = forms.CharField(required=True, label=_('Codice Fiscale'))

    codice_fiscale = ITSocialSecurityNumberField(required=True, label=_('Codice Fiscale'))

    accertamento_casellario = forms.BooleanField(required=False, label=_('Accertamento casellario'))
    accertamento_universita = forms.BooleanField(required=False, label=_('accertamento universita'))

    ritiro_agenda = forms.BooleanField(required=False, label=_('Ritito agenda'))
    invio_tesserino = forms.BooleanField(required=False, label=_('Invio tesserino'))

    class Meta:
        exclude = [ "accertamento_casellario", "accertamento_universita", ]

    def clean(self, *args, **kwargs):

        data = super(UserRegistrationForm, self).clean(*args, **kwargs)

        says_is_psicologo_lavoro = data["says_is_psicologo_lavoro"]
        says_is_psicologo_clinico = data["says_is_psicologo_clinico"]
        says_is_psicologo_forense = data["says_is_psicologo_forense"]
        says_is_dottore_tecniche_psicologiche = data["says_is_dottore_tecniche_psicologiche"]

        qualifica = (says_is_psicologo_lavoro or says_is_psicologo_clinico or says_is_psicologo_forense or says_is_dottore_tecniche_psicologiche)
    
        data_iscrizione = data["register_subscription_date"]


        if (data_iscrizione and not qualifica) or (not data_iscrizione and qualifica):

            msg = _("If you specify the date when you subscribed the register, you must also provide what kind of psychologist you are, and vice-versa")

            raise ValidationError(msg)


        return data


class UserProfileForm(forms.Form):

    fieldsets = {
        "basic" : [ "uses_nickname", "description", "image", ],
        "contacts": ["indirizzo_residenza", "citta_residenza", "cap_residenza", "provincia_residenza", "indirizzo_domicilio", "citta_domicilio", "cap_domicilio", "provincia_domicilio", "indirizzo_studio", "citta_studio", "cap_studio", "provincia_studio",],
        "contacts2": [ "tel_residenza", "tel_domicilio", "tel_ufficio", "tel_cellulare", "indirizzo_email", "indirizzo_pec", "sito_internet"]
    }



    location = forms.ModelChoiceField(required=False, queryset=Location.objects.order_by("name"), label=_('Location, if applicable'),
                        help_text=u"Se compare nella lista, scegli la zona della città in cui risiedi")
        
    uses_nickname = forms.BooleanField(label=_(u'I want only my nickname to be publicly shown'), help_text=u"Indica se preferisci che nel sito venga mostrato esclusivamente il tuo nome utente", required=False)

    description = forms.CharField(required=False, label=_('Description'), widget=forms.Textarea(),
                                  help_text=u"Una breve descrizione di te, che apparirà nel tuo profilo")
    image = forms.ImageField(required=False, label=_('Your image'),
                             help_text="L'immagine che scegli verrà ridimensionata nelle dimensioni di 100x100 pixel")

    indirizzo_residenza = forms.CharField(required=True, label=_('Indirizzo'))
    citta_residenza = forms.CharField(required=True, label=_(u'Città'))
    cap_residenza = forms.CharField(required=True, label=_('CAP'))
    provincia_residenza = forms.CharField(required=True, label=_('Provincia'))

    indirizzo_domicilio = forms.CharField(required=False, label=_('Indirizzo'))
    citta_domicilio = forms.CharField(required=False, label=_(u'Città'))
    cap_domicilio = forms.CharField(required=False, label=_('CAP'))
    provincia_domicilio = forms.CharField(required=False, label=_('Provincia'))

    indirizzo_studio = forms.CharField(required=False, label=_('Indirizzo'))
    
    #citta_studio = forms.CharField(required=False, label=_(u'Città'))
    citta_studio = forms.ModelChoiceField(required=False, label=_(u'Città'), queryset = Comuni.objects.all())

    cap_studio = forms.CharField(required=False, label=_('CAP'))
    provincia_studio = forms.CharField(required=False, label=_('Provincia'))

    denominazione_studio = forms.CharField(required=False, label=_('Inserire la denominazione dello studio'), widget=forms.Textarea())
    coord_lat = forms.FloatField(required=False, label=_('latitudine studio'))
    coord_long = forms.FloatField(required=False, label=_('longitudine studio'))

    consegna_corrispondenza = forms.ChoiceField(choices=Recapito.TIPI_CORRISPONDENZA, required=False, label=_('consegna corrispondenza'))

    tel_residenza = forms.CharField(required=False, label=_(u'Telefono residenza'))
    tel_domicilio = forms.CharField(required=False, label=_(u'Telefono domicilio'))
    tel_ufficio = forms.CharField(required=False, label=_(u'Telefono ufficio'))
    tel_cellulare = forms.CharField(required=False, label=_(u'Telefono cellulare'))
    tel_residenza = forms.CharField(required=False, label=_(u'Telefono residenza'))
    indirizzo_email = forms.EmailField(required=False, label=_(u'Email'))
    indirizzo_pec = forms.CharField(required=False, label=_(u'Email PEC'))
    sito_internet = forms.URLField(required=False, label=_(u'Sito internet'))

    def clean(self, *args, **kwargs):

        data = super(UserProfileForm, self).clean(*args, **kwargs)
        test_email = data["indirizzo_email"]
        test_pec = data["indirizzo_pec"] 

        if (len(test_email) > 254):
            msg = _("verificare la email troppo lunga")
            raise ValidationError(msg)

        if (len(test_pec) > 254):
            msg = _("verificare la PEC troppo lunga")
            raise ValidationError(msg)

        return data




