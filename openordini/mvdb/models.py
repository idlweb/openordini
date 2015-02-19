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
        verbose_name = 'comune'
        verbose_name_plural = 'comuni'

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.codice_comune_istat)


class Provincie(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.TextField()
    slug = models.CharField(max_length=255)
    abbr = models.CharField(max_length=21)
    codice_provincia_istat = models.CharField(max_length=255)
    codice_regione_istat = models.CharField(max_length=255)

    class Meta:
        db_table = 'provincie'
        verbose_name = 'provincia'
        verbose_name_plural = 'provincie'

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.codice_provincia_istat)


class Regioni(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    codice_regione_istat = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'regioni'
        verbose_name = 'regione'
        verbose_name_plural = 'regioni'

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.codice_regione_istat)

# Create your models here.
