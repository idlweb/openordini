# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recapiti'
        db.create_table(u'oo_users_recapiti', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recapiti_psicologo', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['oo_users.UserProfile'], unique=True)),
            ('tel_residenza', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tel_domicilio', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tel_ufficio', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tel_cellulare', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('indirizzo_email', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('indirizzo_pec', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'oo_users', ['Recapiti'])

        # Adding model 'caratteristiche_gestione'
        db.create_table(u'oo_users_caratteristiche_gestione', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gestione_psicologo', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['oo_users.UserProfile'], unique=True)),
            ('ritiro_agenda', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invio_tesserino', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('numero_faldone', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'oo_users', ['caratteristiche_gestione'])

        # Adding model 'ExtraPeople'
        db.create_table(u'oo_users_extrapeople', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('anagrafica_extra', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['oo_users.UserProfile'], unique=True)),
            ('indirizzo_residenza', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('citta_residenza', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('indirizzo_domicilio', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('citta_domicilio', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('cap', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('provincia_domicilio', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('codice_fiscale', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('accertamento_casellario', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accertamento_universita', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'oo_users', ['ExtraPeople'])

        # Adding model 'Trasferimenti'
        db.create_table(u'oo_users_trasferimenti', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trasferimenti_psicologo', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['oo_users.UserProfile'], unique=True)),
            ('trasferimento_data', self.gf('django.db.models.fields.DateField')(max_length=25)),
            ('delibera_trasferiemnto', self.gf('django.db.models.fields.IntegerField')()),
            ('data_delibera_trasferiemnto', self.gf('django.db.models.fields.DateField')()),
            ('motivazione_trasferimento', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('regione_trasferimento', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tassa_trasferimento', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'oo_users', ['Trasferimenti'])

        # Adding model 'PsicologoTitoli'
        db.create_table(u'oo_users_psicologotitoli', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('psicologo_registrato', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['oo_users.ExtraPeople'], unique=True)),
            ('titolo_laurea', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('articolo_tre', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('articolo_tre_delibera', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('articolo_tre_data', self.gf('django.db.models.fields.DateField')()),
            ('articolo_tre_note', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('iscrizione_albo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('laurea_specializzazione', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data_iscrizione_albo', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'oo_users', ['PsicologoTitoli'])


    def backwards(self, orm):
        # Deleting model 'Recapiti'
        db.delete_table(u'oo_users_recapiti')

        # Deleting model 'caratteristiche_gestione'
        db.delete_table(u'oo_users_caratteristiche_gestione')

        # Deleting model 'ExtraPeople'
        db.delete_table(u'oo_users_extrapeople')

        # Deleting model 'Trasferimenti'
        db.delete_table(u'oo_users_trasferimenti')

        # Deleting model 'PsicologoTitoli'
        db.delete_table(u'oo_users_psicologotitoli')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.location': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        u'newscache.news': {
            'Meta': {'object_name': 'News'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'generating_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'generating_content_type_set_for_news'", 'to': u"orm['contenttypes.ContentType']"}),
            'generating_object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'news_type': ('django.db.models.fields.CharField', [], {'default': "'INST'", 'max_length': '4'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'related_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_content_type_set_for_news'", 'to': u"orm['contenttypes.ContentType']"}),
            'related_object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '512'})
        },
        u'oo_users.caratteristiche_gestione': {
            'Meta': {'object_name': 'caratteristiche_gestione'},
            'gestione_psicologo': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['oo_users.UserProfile']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invio_tesserino': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numero_faldone': ('django.db.models.fields.IntegerField', [], {}),
            'ritiro_agenda': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'oo_users.extrapeople': {
            'Meta': {'object_name': 'ExtraPeople'},
            'accertamento_casellario': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accertamento_universita': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'anagrafica_extra': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['oo_users.UserProfile']", 'unique': 'True'}),
            'cap': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'citta_domicilio': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'citta_residenza': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'codice_fiscale': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirizzo_domicilio': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'indirizzo_residenza': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'provincia_domicilio': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'oo_users.psicologotitoli': {
            'Meta': {'object_name': 'PsicologoTitoli'},
            'articolo_tre': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'articolo_tre_data': ('django.db.models.fields.DateField', [], {}),
            'articolo_tre_delibera': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'articolo_tre_note': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'data_iscrizione_albo': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iscrizione_albo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'laurea_specializzazione': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'psicologo_registrato': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['oo_users.ExtraPeople']", 'unique': 'True'}),
            'titolo_laurea': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'oo_users.recapiti': {
            'Meta': {'object_name': 'Recapiti'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirizzo_email': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'indirizzo_pec': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'recapiti_psicologo': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['oo_users.UserProfile']", 'unique': 'True'}),
            'tel_cellulare': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tel_domicilio': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tel_residenza': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tel_ufficio': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'oo_users.trasferimenti': {
            'Meta': {'object_name': 'Trasferimenti'},
            'data_delibera_trasferiemnto': ('django.db.models.fields.DateField', [], {}),
            'delibera_trasferiemnto': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motivazione_trasferimento': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'regione_trasferimento': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tassa_trasferimento': ('django.db.models.fields.FloatField', [], {}),
            'trasferimenti_psicologo': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['oo_users.UserProfile']", 'unique': 'True'}),
            'trasferimento_data': ('django.db.models.fields.DateField', [], {'max_length': '25'})
        },
        u'oo_users.userprofile': {
            'Meta': {'object_name': 'UserProfile', '_ormbases': [u'users.UserProfile']},
            'register_subscription_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'says_is_asl_employee': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'says_is_psicologo_clinico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'says_is_psicologo_forense': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'says_is_psicologo_lavoro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'says_is_self_employed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.UserProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'people.person': {
            'Meta': {'object_name': 'Person'},
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'birth_location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'op_politician_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "u'users_user_profile'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['people.Person']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'privacy_level': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'says_is_politician': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'uses_nickname': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wants_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['oo_users']