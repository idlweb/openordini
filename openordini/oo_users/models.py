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
    says_is_dottore_tecniche_psicologiche = models.BooleanField(default=False, verbose_name=_("dottore in tecniche psicologiche"), help_text=_(u"notifica l'amministratore che ha il titolo di dottore in tecniche psicologiche"))
    says_is_asl_employee = models.BooleanField(default=False, verbose_name=_("ASL employee"), help_text=_(u"notifica l'amministratore che è un dipendente ASL"))
    says_is_self_employed = models.BooleanField(default=False, verbose_name=_("psicologo clinico"), help_text=_(u"notifica l'amministratore che è un libero professionista"))
    register_subscription_date = models.DateField(default=None, blank=True, null=True, verbose_name=_(u"register subscription date"), help_text=_(u"la data in cui si è registrato all'albo"))
    wants_commercial_newsletter = models.BooleanField(default=False, verbose_name=_("wants commercial newsletter"))
    

    @property
    def committee_charges(self):

        comm = []
    
        try:
            all_comm = municipality.committees.as_institution()

            comm = self.person.institutioncharge_set.filter(institution__in=all_comm)
        
        except ObjectDoesNotExist:
            pass

        return comm

    def __unicode__(self):
        return self.person.first_name + ' - ' + self.person.last_name 

    class Meta:
        verbose_name = _("scheda psicologo")
        verbose_name_plural = _("schede psicologi")


class ExtraPeople(models.Model):

    anagrafica_extra = models.OneToOneField(UserProfile, related_name="anagrafica")
    indirizzo_residenza = models.CharField(_('indirizzo residenza'), help_text=_(u"inserire l'indirizzo residenza") , max_length=128)
    citta_residenza = models.CharField(_(u'città residenza'), help_text=_(u"inserire la città residenza") , max_length=128)
    cap_residenza = models.CharField(_('CAP residenza'), help_text=_(u"inserire il CAP residenza") , max_length=5)
    provincia_residenza = models.CharField(_('provincia domicilio'), help_text=_(u"inserire la provincia residenza") , max_length=128)

    indirizzo_domicilio = models.CharField(_('indirizzo domicilio'), help_text=_(u"inserire l'indirizzo domicilio") , max_length=128)
    citta_domicilio = models.CharField(_(u'città domicilio'), help_text=_(u"inserire la città domicilio") , max_length=128)
    cap_domicilio = models.CharField(_('CAP domicilio'), help_text=_(u"inserire il CAP domicilio") , max_length=5)
    provincia_domicilio = models.CharField(_('provincia domicilio'), help_text=_(u"inserire la provincia domicilio") , max_length=128)

    codice_fiscale = models.CharField(_('codice fiscale'), help_text=_(u"inserire il codice fiscale") , max_length=16)
    accertamento_casellario = models.BooleanField(_('verifica casellario giudiziario'), help_text=_(u"accertamento casellario"))
    accertamento_universita = models.BooleanField(_('verifica conseguimento titolo accademico'), help_text=_(u"accertamento universita"))
    
    def __unicode__(self):
        return self.anagrafica_extra.person.first_name + ' - ' + self.anagrafica_extra.person.last_name + ' - ' + self.codice_fiscale

    class Meta:
        verbose_name = _("anagrafica aggiuntiva")
        verbose_name_plural = _("anagrafiche aggiuntive")


class Recapito(models.Model):
    recapiti_psicologo = models.OneToOneField(UserProfile, related_name="recapiti")
    tel_residenza = models.CharField(_('telefono residenza'), help_text=_(u"inserire il telefono della residenza") , max_length=10)
    tel_domicilio = models.CharField(_('telefono domicilio'), help_text=_(u"inserire il telefono del domicilio") , max_length=10)
    tel_ufficio = models.CharField(_('telefono ufficio'), help_text=_(u"inserire il telefono ufficio") , max_length=10)
    tel_cellulare = models.CharField(_('numero cellulare'), help_text=_(u"inserire il numero del cellulare") , max_length=10)
    indirizzo_email = models.CharField(_('indirizzo email'), help_text=_(u"inserire l'indirizzo email") , max_length=200)
    indirizzo_pec = models.CharField(_('indirizzo pec'), help_text=_(u"inserire l'indirizzo pec") , max_length=20)
    sito_internet = models.URLField(_('indirizzo sito'), help_text=_(u"inserire sito internet"), )
    
    def __unicode__(self):
        return self.recapiti_psicologo.person.first_name + ' - ' +self.recapiti_psicologo.person.last_name #self.codice_fiscale


    class Meta:
        verbose_name = _("recapito")
        verbose_name_plural = _("recapiti")

class Caratteristiche_gestione(models.Model):
    gestione_psicologo = models.OneToOneField(UserProfile, related_name="gestione")	
    ritiro_agenda = models.BooleanField(_('ritiro agenda'), help_text=_(u"ritiro agenda"))
    invio_tesserino = models.BooleanField(_('invio tesserino'), help_text=_(u"invio tesserino"))
    numero_faldone = models.IntegerField(_('numero_faldone'), help_text=_(u"numero faldone"))

    def __unicode__(self):
        return self.gestione_psicologo.person.first_name + ' - ' + self.gestione_psicologo.person.last_name 

    class Meta:
        verbose_name = _("caratteristiche di gestione")
        verbose_name_plural = _("caratteristiche di gestione")

class Trasferimento(models.Model):
    trasferimenti_psicologo = models.OneToOneField(UserProfile, related_name="trasferimenti")
    trasferimento_data = models.DateField(_('data di trasferimento albo'), help_text=_(u"trasferimento data") , max_length=25)
    delibera_trasferiemnto =  models.IntegerField(_('delibera trasferimento'), help_text=_(u"delibera trasferimento"))
    data_delibera_trasferiemnto = models.DateField(_('data delibera trasferimento'), help_text=_(u"data delibera") )
    motivazione_trasferimento = models.CharField(_('motivazione trasferimento'), help_text=_(u"motivazione delibera"), max_length=255)
    regione_trasferimento = models.CharField(_('regione trasferimento'), help_text=_(u"regione trasferimento") , max_length=50)
    tassa_trasferimento = models.FloatField(_('tassa di trasferimento'))
    
    def __unicode__(self):
        return self.trasferimenti_psicologo.person.first_name + ' - ' + self.trasferimenti_psicologo.person.last_name 


    class Meta:
        verbose_name = _("trasferimento")
        verbose_name_plural = _("trasferimenti")

class PsicologoTitoli(models.Model):
    """
    This model describes a user's profile.
  
    """
    TIPI_FACOLTA = Choices(
        ('psicologia', 'psicologia', _('psicologia')),
        ('filosofia pedagogica', 'filosofia pedagogica', _('filosofia')),
        ('medicina', 'medicina', _('medicina')),
        ('altro', 'altro', _('altro'))
    )

    # This field is required.
    psicologo_registrato = models.OneToOneField(UserProfile, related_name="titoli")
    titolo_laurea = models.CharField(_('titolo laurea'), choices=TIPI_FACOLTA, help_text=_(u"titolo laurea") , max_length=50)
    data_iscrizione_albo = models.DateField(_("data iscrizione all'albo"), help_text=_(u"data iscrizione albo") )
    articolo_tre = models.BooleanField(_('presenza articolo 3'), help_text=_(u"articolo tre"))
    articolo_tre_delibera = models.IntegerField(_('delibera art. 3'), help_text=_(u"articolo tre delibera"), max_length=5)
    articolo_tre_data = models.DateField(_("data delibera art 3"), help_text=_(u"articolo tre data") )
    articolo_tre_note = models.CharField(_("note per l'articolo 3"), help_text=_(u"articolo tre note"), max_length=128)
    iscrizione_albo = models.BooleanField(_('avvenuta iscrizione'), default=False,
                                        help_text=u"Indica se l'utente si è iscritto all'albo")
    laurea_specializzazione = models.BooleanField(_('laurea specializzazione'), default=False,
                                        help_text=u"Indica se è stata conseguita la specializzazione")
    data_iscrizione_albo = models.DateField(_('data iscrizione albo'), help_text=_(u"Provide, if you are already a registered member"))
    
    def __unicode__(self):
        return self.psicologo_registrato.person.first_name + ' - ' + self.psicologo_registrato.person.last_name 


    class Meta:
        verbose_name = _("titoli psicologo")
        verbose_name_plural = _("titoli psicologi")
    
    
      


