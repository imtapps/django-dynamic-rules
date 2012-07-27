# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Rule.secondary_object_id'
        db.add_column('dynamic_rules_rule', 'secondary_object_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Rule.secondary_object_id'
        db.delete_column('dynamic_rules_rule', 'secondary_object_id')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dynamic_rules.rule': {
            'Meta': {'object_name': 'Rule'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'dynamic_fields': ('django_fields.fields.PickleField', [], {}),
            'group_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'secondary_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'})
        }
    }

    complete_apps = ['dynamic_rules']