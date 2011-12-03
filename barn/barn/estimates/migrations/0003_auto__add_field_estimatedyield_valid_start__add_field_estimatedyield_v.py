# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'EstimatedYield.valid_start'
        db.add_column('estimates_estimatedyield', 'valid_start', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2010, 1, 1, 0, 0)), keep_default=False)

        # Adding field 'EstimatedYield.valid_end'
        db.add_column('estimates_estimatedyield', 'valid_end', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2011, 1, 1, 0, 0)), keep_default=False)

        # Adding field 'EstimatedCost.valid_start'
        db.add_column('estimates_estimatedcost', 'valid_start', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2010, 1, 1, 0, 0)), keep_default=False)

        # Adding field 'EstimatedCost.valid_end'
        db.add_column('estimates_estimatedcost', 'valid_end', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2011, 1, 1, 0, 0)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'EstimatedYield.valid_start'
        db.delete_column('estimates_estimatedyield', 'valid_start')

        # Deleting field 'EstimatedYield.valid_end'
        db.delete_column('estimates_estimatedyield', 'valid_end')

        # Deleting field 'EstimatedCost.valid_start'
        db.delete_column('estimates_estimatedcost', 'valid_start')

        # Deleting field 'EstimatedCost.valid_end'
        db.delete_column('estimates_estimatedcost', 'valid_end')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'estimates.estimatedcost': {
            'Meta': {'object_name': 'EstimatedCost'},
            'cost_per_pound': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'estimated': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'should_be_used': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'valid_end': ('django.db.models.fields.DateField', [], {}),
            'valid_start': ('django.db.models.fields.DateField', [], {}),
            'variety': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['farmingconcrete.Variety']"})
        },
        'estimates.estimatedyield': {
            'Meta': {'object_name': 'EstimatedYield'},
            'estimated': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pounds_per_plant': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'should_be_used': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'valid_end': ('django.db.models.fields.DateField', [], {}),
            'valid_start': ('django.db.models.fields.DateField', [], {}),
            'variety': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['farmingconcrete.Variety']"})
        },
        'farmingconcrete.variety': {
            'Meta': {'ordering': "['name']", 'object_name': 'Variety'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmingconcrete_variety_added'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'needs_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmingconcrete_variety_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['estimates']
