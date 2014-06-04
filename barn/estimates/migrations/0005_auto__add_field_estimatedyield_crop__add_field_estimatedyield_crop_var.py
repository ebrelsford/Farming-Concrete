# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EstimatedYield.crop'
        db.add_column(u'estimates_estimatedyield', 'crop',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crops.Crop'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'EstimatedYield.crop_variety'
        db.add_column(u'estimates_estimatedyield', 'crop_variety',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crops.Variety'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'EstimatedCost.crop'
        db.add_column(u'estimates_estimatedcost', 'crop',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crops.Crop'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'EstimatedCost.crop_variety'
        db.add_column(u'estimates_estimatedcost', 'crop_variety',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crops.Variety'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EstimatedYield.crop'
        db.delete_column(u'estimates_estimatedyield', 'crop_id')

        # Deleting field 'EstimatedYield.crop_variety'
        db.delete_column(u'estimates_estimatedyield', 'crop_variety_id')

        # Deleting field 'EstimatedCost.crop'
        db.delete_column(u'estimates_estimatedcost', 'crop_id')

        # Deleting field 'EstimatedCost.crop_variety'
        db.delete_column(u'estimates_estimatedcost', 'crop_variety_id')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'crops.crop': {
            'Meta': {'ordering': "['name']", 'object_name': 'Crop'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'crops_crop_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'needs_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'crops_crop_updated'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'crops.variety': {
            'Meta': {'ordering': "['name']", 'object_name': 'Variety'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'crops_variety_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'crop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Crop']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'needs_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'crops_variety_updated'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'estimates.estimatedcost': {
            'Meta': {'object_name': 'EstimatedCost'},
            'cost_per_pound': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'crop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Crop']", 'null': 'True', 'blank': 'True'}),
            'crop_variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Variety']", 'null': 'True', 'blank': 'True'}),
            'estimated': ('django.db.models.fields.DateField', [], {}),
            'garden_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.GardenType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'should_be_used': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'valid_end': ('django.db.models.fields.DateField', [], {}),
            'valid_start': ('django.db.models.fields.DateField', [], {}),
            'variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Variety']"})
        },
        u'estimates.estimatedyield': {
            'Meta': {'object_name': 'EstimatedYield'},
            'crop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Crop']", 'null': 'True', 'blank': 'True'}),
            'crop_variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Variety']", 'null': 'True', 'blank': 'True'}),
            'estimated': ('django.db.models.fields.DateField', [], {}),
            'garden_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.GardenType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pounds_per_plant': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'should_be_used': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'valid_end': ('django.db.models.fields.DateField', [], {}),
            'valid_start': ('django.db.models.fields.DateField', [], {}),
            'variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Variety']"})
        },
        u'farmingconcrete.gardentype': {
            'Meta': {'ordering': "['name']", 'object_name': 'GardenType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'farmingconcrete.variety': {
            'Meta': {'ordering': "['name']", 'object_name': 'Variety'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'farmingconcrete_variety_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'needs_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'farmingconcrete_variety_updated'", 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['estimates']