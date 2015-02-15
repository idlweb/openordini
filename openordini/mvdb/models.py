from __future__ import unicode_literals

from django.db import models

class Comuni(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.TextField()
    slug = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    codice_provincia_istat = models.CharField(max_length=255)
    codice_comune_istat = models.CharField(max_length=255)
    codice_alfanumerico_istat = models.CharField(max_length=255)
    capoluogo_provincia = models.IntegerField()
    capoluogo_regione = models.IntegerField()
    class Meta:
        db_table = 'comuni'

class Provincie(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.TextField()
    slug = models.CharField(max_length=255)
    abbr = models.CharField(max_length=21)
    codice_provincia_istat = models.CharField(max_length=255)
    codice_regione_istat = models.CharField(max_length=255)
    class Meta:
        db_table = 'provincie'

class Regioni(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    codice_regione_istat = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'regioni'

# Create your models here.
