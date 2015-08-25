from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User, Group
from sendgrid.models import EmailMessage

class recordo_login_by_email(models.Model):  
    utente_email = models.ForeignKey(User)
    password_email = models.CharField(max_length=255)
    username_email = models.CharField(max_length=255)
    ref_email = models.ForeignKey(EmailMessage)
