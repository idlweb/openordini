# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import permalink
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from model_utils import Choices
from open_municipio.users.models import UserProfile as OMUserProfile
from open_municipio.people.models import municipality


class UserProfile(OMUserProfile):
    says_is_psicologo_clinico = models.BooleanField(default=False, verbose_name=_("psicologo clinico"), help_text=_(u"notifica l'amministratore che è uno psicologo clinico"))
    says_is_psicologo_lavoro = models.BooleanField(default=False, verbose_name=_("psicologo del lavoro"), help_text=_(u"notifica l'amministratore che è uno psicologo del lavoro'"))
    says_is_psicologo_forense = models.BooleanField(default=False, verbose_name=_("psicologo forense"), help_text=_(u"notifica l'amministratore che è uno psicologo forense"))
    says_is_asl_employee = models.BooleanField(default=False, verbose_name=_("ASL employee"), help_text=_(u"notifica l'amministratore che è un dipendente ASL"))
    says_is_self_employed = models.BooleanField(default=False, verbose_name=_("psicologo clinico"), help_text=_(u"notifica l'amministratore che è un libero professionista"))
    register_subscription_date = models.DateField(default=None, blank=True, null=True, verbose_name=_(u"register subscription date"), help_text=_(u"la data in cui si è registrato all'albo"))

    @property
    def committee_charges(self):

        comm = []
    
        try:
            all_comm = municipality.committees.as_institution()

            comm = self.person.institutioncharge_set.filter(institution__in=all_comm)
        
        except ObjectDoesNotExist:
            pass

        return comm


    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")


class ExtraPeople(models.Model):
	anagrafica_extra = models.OneToOneField(UserProfile)
	indirizzo_residenza = models.CharField(_('indirizzo di resicdenza'), help_text=_(u"inserire l'indirizzo di residenza") , max_length=128)
	citta_residenza = models.CharField(_('città di residenza'), help_text=_(u"inserire la città di residenza") , max_length=128)
	indirizzo_domicilio = models.CharField(_('indirizzo del domicilio'), help_text=_(u"inserire l'indirizzo del domicilio") , max_length=128)
	citta_domicilio = models.CharField(_('città di domicilio'), help_text=_(u"inserire la città di domicilio") , max_length=128)
	cap = models.CharField(_('CAP'), help_text=_(u"inserire il CAP") , max_length=5)
	provincia_domicilio = models.CharField(_('provincia del domicilio'), help_text=_(u"inserire la provincia del domicilio") , max_length=128)
	codice_fiscale = models.CharField(_('codice fiscale'), help_text=_(u"inserire il codice fiscale") , max_length=16)
	accertamento_casellario = models.BooleanField(_('verifica casellario giudiziario'), help_text=_(u""))
	accertamento_universita = models.BooleanField(_('verifica conseguimento titolo accademico'), help_text=_(u""))
	
	
	#class Meta:
        #verbose_name = _("extra people")
        #verbose_name_plural = _("extra people")

class Recapiti(models.Model):
	recapiti_psicologo = models.OneToOneField(UserProfile)
	tel_residenza = models.CharField(_('telefono residenza'), help_text=_(u"inserire il telefono della residenza") , max_length=10)
	tel_domicilio = models.CharField(_('telefono domicilio'), help_text=_(u"inserire il telefono del domicilio") , max_length=10)
	tel_ufficio = models.CharField(_('telefono ufficio'), help_text=_(u"inserire il telefono ufficio") , max_length=10)
	tel_cellulare = models.CharField(_('numero cellulare'), help_text=_(u"inserire il numero del cellulare") , max_length=10)
	indirizzo_email = models.CharField(_('indirizzo email'), help_text=_(u"inserire l'indirizzo email") , max_length=20)
	indirizzo_pec = models.CharField(_('indirizzo pec'), help_text=_(u"inserire l'indirizzo pec") , max_length=20)
    
	#class Meta:
        #verbose_name = _("recapito")
        #verbose_name_plural = _("recapiti")

class caratteristiche_gestione(models.Model):
	gestione_psicologo = models.OneToOneField(UserProfile)	
	ritiro_agenda = models.BooleanField(_('numero cellulare'), help_text=_(u""))
	invio_tesserino = models.BooleanField(_('indirizzo email'), help_text=_(u""))
	numero_faldone = models.IntegerField(_('indirizzo pec'), help_text=_(u""))


class Trasferimenti(models.Model):
	trasferimenti_psicologo = models.OneToOneField(UserProfile)
	trasferimento_data = models.DateField(_('data di trasferimento albo'), help_text=_(u"") , max_length=25)
	delibera_trasferiemnto =  models.IntegerField(_('delibera trasferimento'), help_text=_(u""))
	data_delibera_trasferiemnto = models.DateField(_('data delibera trasferimento'), help_text=_(u"") )
	motivazione_trasferimento = models.CharField(_('motivazione trasferimento'), help_text=_(u""), max_length=255)
	regione_trasferimento = models.CharField(_('regione trasferimento'), help_text=_(u"") , max_length=50)
	tassa_trasferimento = models.FloatField(_('tassa di trasferimento'))	


class PsicologoTitoli(models.Model):
    """
    This model describes a user's profile.
  
    """
    TIPI_FACOLTA = Choices(
        (1, 'psicologia', _('predefinita')),
        (2, 'filosofia pedagogica', _('filosofia')),
        (3, 'medicina', _('medicina')),
        (4, 'altro', _('altro'))
    )

    # This field is required.
    psicologo_registrato = models.OneToOneField(ExtraPeople)
    titolo_laurea = models.CharField(_('titolo laurea'), choices=TIPI_FACOLTA, help_text=_(u"") , max_length=50)
    data_iscrizione_albo = models.DateField(_("data iscrizione all'albo"), help_text=_(u"") )
    articolo_tre = models.BooleanField(_('presenza articolo 3'), help_text=_(u""))
    articolo_tre_delibera = models.IntegerField(_('delibera art. 3'), help_text=_(u""), max_length=5)
    articolo_tre_data = models.DateField(_("data delibera art 3"), help_text=_(u"") )
    articolo_tre_note = models.CharField(_("note per l'articolo 3"), help_text=_(u""), max_length=128)
    iscrizione_albo = models.BooleanField(_('avvenuta iscrizione'), default=False,
                                        help_text=u"Indica se l'utente si è iscritto all'albo")
    laurea_specializzazione = models.BooleanField(_('laurea specializzazione'), default=False,
                                        help_text=u"Indica se è stata conseguita la specializzazione")
    data_iscrizione_albo = models.DateField(_('data iscrizione albo'), help_text=_(u""))

    
    
      


