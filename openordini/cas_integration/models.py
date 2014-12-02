from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

class Capability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name="capabilities", verbose_name=_("user"))
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("name"))
    link = models.URLField(max_length=200, null=False, blank=False, verbose_name=_("url"))
