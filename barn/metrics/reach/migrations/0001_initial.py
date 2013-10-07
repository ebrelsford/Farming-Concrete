# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProgramFeature'
        db.create_table(u'reach_programfeature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('universal', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'reach', ['ProgramFeature'])

        # Adding model 'ProgramReach'
        db.create_table(u'reach_programreach', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'reach_programreach_added', null=True, to=orm['auth.User'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'reach_programreach_updated', null=True, to=orm['auth.User'])),
            ('garden', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farmingconcrete.Garden'], null=True, blank=True)),
            ('recorded', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('recorded_start', self.gf('django.db.models.fields.DateField')()),
            ('hours_each_day', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1)),
            ('collaborated_with_organization', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('collaboration_first', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('age_10', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_10_14', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_15_19', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_20_24', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_25_34', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_35_44', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_45_54', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_55_64', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_65', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gender_male', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gender_female', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gender_other', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('zipcode_inside', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('zipcode_outside', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'reach', ['ProgramReach'])

        # Adding M2M table for field features on 'ProgramReach'
        m2m_table_name = db.shorten_name(u'reach_programreach_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('programreach', models.ForeignKey(orm[u'reach.programreach'], null=False)),
            ('programfeature', models.ForeignKey(orm[u'reach.programfeature'], null=False))
        ))
        db.create_unique(m2m_table_name, ['programreach_id', 'programfeature_id'])


    def backwards(self, orm):
        # Deleting model 'ProgramFeature'
        db.delete_table(u'reach_programfeature')

        # Deleting model 'ProgramReach'
        db.delete_table(u'reach_programreach')

        # Removing M2M table for field features on 'ProgramReach'
        db.delete_table(db.shorten_name(u'reach_programreach_features'))


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
        u'farmingconcrete.garden': {
            'Meta': {'object_name': 'Garden'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'gardenid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.GardenType']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        u'farmingconcrete.gardentype': {
            'Meta': {'ordering': "['name']", 'object_name': 'GardenType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'reach.programfeature': {
            'Meta': {'object_name': 'ProgramFeature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'universal': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'reach.programreach': {
            'Meta': {'object_name': 'ProgramReach'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'reach_programreach_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'age_10': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_10_14': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_15_19': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_20_24': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_25_34': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_35_44': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_45_54': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_55_64': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_65': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collaborated_with_organization': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collaboration_first': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reach.ProgramFeature']", 'null': 'True', 'blank': 'True'}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']", 'null': 'True', 'blank': 'True'}),
            'gender_female': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gender_male': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gender_other': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hours_each_day': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recorded_start': ('django.db.models.fields.DateField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'reach_programreach_updated'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'zipcode_inside': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zipcode_outside': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['reach']