# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        """Move farmingconcrete.Variety instances to crops.Crop"""
        for variety in orm.Variety.objects.all():
            # Create new Crop
            crop = orm['crops.Crop'](
                name=variety.name,
                needs_moderation=variety.needs_moderation,
                added=variety.added,
                added_by=variety.added_by,
                updated=variety.updated,
                updated_by=variety.updated_by,
            )
            crop.save()

            # Update all existing instance to point to new Crop
            orm['cropcount.Patch'].objects.filter(variety=variety).update(crop=crop)
            orm['estimates.EstimatedCost'].objects.filter(variety=variety).update(crop=crop)
            orm['estimates.EstimatedYield'].objects.filter(variety=variety).update(crop=crop)
            orm['harvestcount.Harvest'].objects.filter(variety=variety).update(crop=crop)
            orm['yumyuck.YumYuck'].objects.filter(vegetable=variety).update(crop=crop)

    def backwards(self, orm):
        """Delete all crops"""
        orm['crops.Crop'].objects.all().delete()

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
        u'cropcount.box': {
            'Meta': {'ordering': "['name']", 'object_name': 'Box'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cropcount_box_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cropcount_box_updated'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'width': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'})
        },
        u'cropcount.patch': {
            'Meta': {'ordering': "['crop']", 'object_name': 'Patch'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cropcount_patch_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'box': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cropcount.Box']"}),
            'crop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Crop']", 'null': 'True', 'blank': 'True'}),
            'crop_variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Variety']", 'null': 'True', 'blank': 'True'}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cropcount_patch_updated'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Variety']", 'null': 'True', 'blank': 'True'})
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
        u'farmingconcrete.gardengroup': {
            'Meta': {'object_name': 'GardenGroup'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gardens': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['farmingconcrete.Garden']", 'through': u"orm['farmingconcrete.GardenGroupMembership']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'farmingconcrete.gardengroupmembership': {
            'Meta': {'object_name': 'GardenGroupMembership'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.GardenGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'harvestcount.harvest': {
            'Meta': {'object_name': 'Harvest'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'harvestcount_harvest_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'crop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Crop']", 'null': 'True', 'blank': 'True'}),
            'crop_variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Variety']", 'null': 'True', 'blank': 'True'}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']", 'null': 'True', 'blank': 'True'}),
            'gardener': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['harvestcount.Gardener']"}),
            'harvested': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plants': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'reportable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'harvestcount_harvest_updated'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Variety']"}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        u'yumyuck.yumyuck': {
            'Meta': {'object_name': 'YumYuck'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'yumyuck_yumyuck_added'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'crop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Crop']", 'null': 'True', 'blank': 'True'}),
            'crop_variety': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crops.Variety']", 'null': 'True', 'blank': 'True'}),
            'garden': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Garden']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'yumyuck_yumyuck_updated'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'vegetable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farmingconcrete.Variety']"}),
            'yuck_after': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'yuck_before': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'yum_after': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'yum_before': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['cropcount', 'harvestcount', 'estimates', 'yumyuck', 'farmingconcrete']
    symmetrical = True
