# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

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
