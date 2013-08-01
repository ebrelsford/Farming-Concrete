# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GardenType'
        db.create_table('farmingconcrete_gardentype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('farmingconcrete', ['GardenType'])

        # Adding model 'Garden'
        db.create_table('farmingconcrete_garden', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farmingconcrete.GardenType'])),
            ('gardenid', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('borough', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('farmingconcrete', ['Garden'])

        # Adding model 'Variety'
        db.create_table('farmingconcrete_variety', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('farmingconcrete', ['Variety'])


    def backwards(self, orm):
        
        # Deleting model 'GardenType'
        db.delete_table('farmingconcrete_gardentype')

        # Deleting model 'Garden'
        db.delete_table('farmingconcrete_garden')

        # Deleting model 'Variety'
        db.delete_table('farmingconcrete_variety')


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
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['farmingconcrete.GardenType']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'farmingconcrete.gardentype': {
            'Meta': {'ordering': "['name']", 'object_name': 'GardenType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'farmingconcrete.variety': {
            'Meta': {'ordering': "['name']", 'object_name': 'Variety'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['farmingconcrete']
