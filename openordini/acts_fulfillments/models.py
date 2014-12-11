import logging
import re
from django.template.defaultfilters import slugify
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from south.modelsinspector import add_ignored_fields
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.template.context import Context
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from model_utils import Choices
from model_utils.managers import InheritanceManager, QueryManager
from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField

from open_municipio.newscache.models import News, NewsTargetMixin

from open_municipio.people.models import Institution, InstitutionCharge, Person, SittingItem
from open_municipio.taxonomy.managers import TopicableManager
from open_municipio.monitoring.models import MonitorizedItem, Monitoring
from open_municipio.acts.models import Act
from django.core.urlresolvers import resolve, reverse

class Fascicolo(Act):
    """
    WRITEME
    """
    INITIATIVE_TYPES = Choices(
        ('COUNSELOR', 'counselor', _('Counselor')),
        ('PRESIDENT', 'president', _('President')),
        ('ASSESSOR', 'assessor', _('City Government Member')),
        ('GOVERNMENT', 'government', _('City Government')),
        ('MAYOR', 'mayor', _('Mayor')),
        ('PSICOLOGO', 'psicologo', _('Psicologo')),
    )

    FINAL_STATUSES = (
        ('APPROVED', _('approved')),
        ('REJECTED', _('rejected')),
        ('SOSPESO', _('sospeso')),
    )

    STATUS = Choices(
        ('PRESENTED', 'presented', _('presented')),
        ('COMMITTEE', 'committee', _('committee')),
        ('COUNCIL', 'council', _('council')),
        ('APPROVED', 'approved', _('approved')),
        ('REJECTED', 'rejected', _('rejected')),
        ('SOSPESO', 'sospeso', _('sospeso')),
    )

    OM_DETAIL_VIEW_NAME = "om_fascicolo_detail"

    status = models.CharField(_('status'), choices=STATUS, max_length=12)
    approval_date = models.DateField(_('approval date'), null=True, blank=True,)
    publication_date = models.DateField(_('publication date'), null=True, blank=True)
    final_idnum = models.CharField(max_length=64, blank=True, null=True, help_text=_("Internal identification string for the deliberation, when approved"))
    execution_date = models.DateField(_('execution date'), null=True, blank=True)
    initiative = models.CharField(_('initiative'), max_length=12, choices=INITIATIVE_TYPES)
    approved_text = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('fascicolo')
        verbose_name_plural = _('fascicoli')
        pass

    @property
    def next_events(self):
        """
        returns the next Events
        """
        from open_municipio.events.models import Event
        #chiave esterna nella tabella esterna
        return Event.future.filter(acts__id=self.id)

    @property
    def next_event(self):
        """
        returns the next Event or None
        """
        return self.next_events[0] if self.next_events else None

##    @models.permalink
##    def get_absolute_url(self):
##        return ('om_deliberation_detail', (), {'slug': str(self.slug)})
##
    

# Create your models here.
