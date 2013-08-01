# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Chart'
        db.create_table('reports_chart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('garden', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farmingconcrete.Garden'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('reports', ['Chart'])


    def backwards(self, orm):
        
        # Deleting model 'Chart'
        db.delete_table('reports_chart')


    models = {
        'farmingconcrete.garden': {
            'Meta': {'object_name': 'Garden'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'gardenid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['farmingconcrete.GardenType']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'farmingconcrete.gardentype': {
            'Meta': {'ordering': "['name']", 'object_name': 'GardenType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'reports.chart': {
            'Meta': {'object_name': 'Chart'},
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['farmingconcrete.Garden']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'reports.sharedreport': {
            'Meta': {'object_name': 'SharedReport'},
            'access_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['farmingconcrete.Garden']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['reports']
