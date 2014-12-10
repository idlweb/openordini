# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.says_is_psicologo_clinico'
        db.add_column(u'oo_users_userprofile', 'says_is_psicologo_clinico',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.says_is_psicologo_lavoro'
        db.add_column(u'oo_users_userprofile', 'says_is_psicologo_lavoro',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.says_is_psicologo_forense'
        db.add_column(u'oo_users_userprofile', 'says_is_psicologo_forense',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.says_is_asl_employee'
        db.add_column(u'oo_users_userprofile', 'says_is_asl_employee',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.says_is_self_employed'
        db.add_column(u'oo_users_userprofile', 'says_is_self_employed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.register_subscription_date'
        db.add_column(u'oo_users_userprofile', 'register_subscription_date',
                      self.gf('django.db.models.fields.DateField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.says_is_psicologo_clinico'
        db.delete_column(u'oo_users_userprofile', 'says_is_psicologo_clinico')

        # Deleting field 'UserProfile.says_is_psicologo_lavoro'
        db.delete_column(u'oo_users_userprofile', 'says_is_psicologo_lavoro')

        # Deleting field 'UserProfile.says_is_psicologo_forense'
        db.delete_column(u'oo_users_userprofile', 'says_is_psicologo_forense')

        # Deleting field 'UserProfile.says_is_asl_employee'
        db.delete_column(u'oo_users_userprofile', 'says_is_asl_employee')

        # Deleting field 'UserProfile.says_is_self_employed'
        db.delete_column(u'oo_users_userprofile', 'says_is_self_employed')

        # Deleting field 'UserProfile.register_subscription_date'
        db.delete_column(u'oo_users_userprofile', 'register_subscription_date')


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
        u'oo_users.userprofile': {
            'Meta': {'object_name': 'UserProfile', '_ormbases': [u'users.UserProfile']},
            'register_subscription_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
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