from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from django_fields import fields as helper_fields

from dynamic_rules import site

class RuleManager(models.Manager):

    def get_by_group_object(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, group_object_id=obj.pk)

    def get_by_key(self, group_object, key):
        return self.get_by_group_object(group_object).filter(key=key)

class Rule(models.Model):
    content_type = models.ForeignKey('contenttypes.ContentType')
    group_object_id = models.PositiveIntegerField(db_index=True)
    group_object = generic.GenericForeignKey(fk_field='group_object_id')

    name = models.CharField(max_length=100)
    key = models.CharField(max_length=50)
    dynamic_fields = helper_fields.PickleField()

    objects = RuleManager()

    def __unicode__(self):
        return self.name

    def run_action(self, validation_object, *args, **kwargs):
        rule_class = site.get_rule_class(self.key)
        rule_class(self, validation_object).run(*args, **kwargs)
