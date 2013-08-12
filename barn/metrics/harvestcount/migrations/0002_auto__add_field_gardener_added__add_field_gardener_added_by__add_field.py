# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Gardener.added'
        db.add_column('harvestcount_gardener', 'added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2011, 5, 25, 14, 41, 52, 290169), blank=True), keep_default=False)

        # Adding field 'Gardener.added_by'
        db.add_column('harvestcount_gardener', 'added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='harvestcount_gardener_added', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Gardener.updated'
        db.add_column('harvestcount_gardener', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2011, 5, 25, 14, 41, 57, 810128), blank=True), keep_default=False)

        # Adding field 'Gardener.updated_by'
        db.add_column('harvestcount_gardener', 'updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='harvestcount_gardener_updated', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Harvest.added_by'
        db.add_column('harvestcount_harvest', 'added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='harvestcount_harvest_added', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Harvest.updated'
        db.add_column('harvestcount_harvest', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2011, 5, 25, 14, 42, 4, 521819), blank=True), keep_default=False)

        # Adding field 'Harvest.updated_by'
        db.add_column('harvestcount_harvest', 'updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='harvestcount_harvest_updated', null=True, to=orm['auth.User']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Gardener.added'
        db.delete_column('harvestcount_gardener', 'added')

        # Deleting field 'Gardener.added_by'
        db.delete_column('harvestcount_gardener', 'added_by_id')

        # Deleting field 'Gardener.updated'
        db.delete_column('harvestcount_gardener', 'updated')

        # Deleting field 'Gardener.updated_by'
        db.delete_column('harvestcount_gardener', 'updated_by_id')

        # Deleting field 'Harvest.added_by'
        db.delete_column('harvestcount_harvest', 'added_by_id')

        # Deleting field 'Harvest.updated'
        db.delete_column('harvestcount_harvest', 'updated')

        # Deleting field 'Harvest.updated_by'
        db.delete_column('harvestcount_harvest', 'updated_by_id')


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
        'farmingconcrete.variety': {
            'Meta': {'ordering': "['name']", 'object_name': 'Variety'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmingconcrete_variety_added'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmingconcrete_variety_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'harvestcount.gardener': {
            'Meta': {'object_name': 'Gardener'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'harvestcount_gardener_added'", 'null': 'True', 'to': "orm['auth.User']"}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['farmingconcrete.Garden']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'harvestcount_gardener_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'harvestcount.harvest': {
            'Meta': {'object_name': 'Harvest'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'harvestcount_harvest_added'", 'null': 'True', 'to': "orm['auth.User']"}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'gardener': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['harvestcount.Gardener']"}),
            'harvested': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plants': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'harvestcount_harvest_updated'", 'null': 'True', 'to': "orm['auth.User']"}),
            'variety': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['farmingconcrete.Variety']"}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        }
    }

    complete_apps = ['harvestcount']
