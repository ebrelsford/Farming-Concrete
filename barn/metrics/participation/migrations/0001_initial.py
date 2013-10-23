# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HoursByGeography'
        db.create_table(u'participation_hoursbygeography', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'participation_hoursbygeography_added', null=True, to=orm['auth.User'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'participation_hoursbygeography_updated', null=True, to=orm['auth.User'])),
            ('garden', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farmingconcrete.Garden'], null=True, blank=True)),
            ('recorded', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('hours', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('recorded_start', self.gf('django.db.models.fields.DateField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'participation', ['HoursByGeography'])

        # Adding model 'Task'
        db.create_table(u'participation_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'participation', ['Task'])

        # Adding model 'TaskHours'
        db.create_table(u'participation_taskhours', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['participation.Task'])),
            ('hours_by_task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['participation.HoursByTask'])),
            ('hours', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'participation', ['TaskHours'])

        # Adding model 'HoursByTask'
        db.create_table(u'participation_hoursbytask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'participation_hoursbytask_added', null=True, to=orm['auth.User'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'participation_hoursbytask_updated', null=True, to=orm['auth.User'])),
            ('garden', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farmingconcrete.Garden'], null=True, blank=True)),
            ('recorded', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recorded_start', self.gf('django.db.models.fields.DateField')()),
            ('task_other', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'participation', ['HoursByTask'])

        # Adding model 'Project'
        db.create_table(u'participation_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('garden', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farmingconcrete.Garden'])),
        ))
        db.send_create_signal(u'participation', ['Project'])

        # Adding model 'ProjectHours'
        db.create_table(u'participation_projecthours', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['participation.HoursByProject'])),
            ('hours', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('gardener', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['harvestcount.Gardener'])),
        ))
        db.send_create_signal(u'participation', ['ProjectHours'])

        # Adding model 'HoursByProject'
        db.create_table(u'participation_hoursbyproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'participation_hoursbyproject_added', null=True, to=orm['auth.User'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'participation_hoursbyproject_updated', null=True, to=orm['auth.User'])),
            ('garden', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farmingconcrete.Garden'], null=True, blank=True)),
            ('recorded', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['participation.Project'])),
        ))
        db.send_create_signal(u'participation', ['HoursByProject'])


    def backwards(self, orm):
        # Deleting model 'HoursByGeography'
        db.delete_table(u'participation_hoursbygeography')

        # Deleting model 'Task'
        db.delete_table(u'participation_task')

        # Deleting model 'TaskHours'
        db.delete_table(u'participation_taskhours')

        # Deleting model 'HoursByTask'
        db.delete_table(u'participation_hoursbytask')

        # Deleting model 'Project'
        db.delete_table(u'participation_project')

        # Deleting model 'ProjectHours'
        db.delete_table(u'participation_projecthours')

        # Deleting model 'HoursByProject'
        db.delete_table(u'participation_hoursbyproject')


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
        u'harvestcount.gardener': {
            'Meta': {'object_name': 'Gardener'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'harvestcount_gardener_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'harvestcount_gardener_updated'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'participation.hoursbygeography': {
            'Meta': {'object_name': 'HoursByGeography'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'participation_hoursbygeography_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']", 'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recorded_start': ('django.db.models.fields.DateField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'participation_hoursbygeography_updated'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'participation.hoursbyproject': {
            'Meta': {'object_name': 'HoursByProject'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'participation_hoursbyproject_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['participation.Project']"}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'participation_hoursbyproject_updated'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'participation.hoursbytask': {
            'Meta': {'object_name': 'HoursByTask'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'participation_hoursbytask_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recorded_start': ('django.db.models.fields.DateField', [], {}),
            'task_other': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['participation.Task']", 'through': u"orm['participation.TaskHours']", 'symmetrical': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'participation_hoursbytask_updated'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'participation.project': {
            'Meta': {'object_name': 'Project'},
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'participation.projecthours': {
            'Meta': {'object_name': 'ProjectHours'},
            'gardener': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['harvestcount.Gardener']"}),
            'hours': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['participation.HoursByProject']"})
        },
        u'participation.task': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Task'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'participation.taskhours': {
            'Meta': {'ordering': "('task__name',)", 'object_name': 'TaskHours'},
            'hours': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hours_by_task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['participation.HoursByTask']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['participation.Task']"})
        }
    }

    complete_apps = ['participation']