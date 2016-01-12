from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User, Group
from sendgrid.models import EmailMessage
from django.utils.translation import ugettext_lazy as _

class recordo_login_by_email(models.Model):  
    utente_email = models.ForeignKey(User)
    password_email = models.CharField(max_length=255)
    username_email = models.CharField(max_length=255)
    ref_email = models.ForeignKey(EmailMessage)
    
def __unicode__(self):
        return self.username_email


class Meta:
    verbose_name = _("credenziali da email")
    verbose_name_plural = _("credenziali da email")
