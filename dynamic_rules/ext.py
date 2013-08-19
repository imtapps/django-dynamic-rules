
"""
Helper Extensions for Dynamic Rules
"""

from django.db import models
from django.contrib.contenttypes.models import ContentType

class RuleExtensionManager(models.Manager):
    """
    RuleExtensionManager can be used by any model that needs to plug into
    the dynamic rules in someway

    A model that uses this manager must include the following:

    rule = models.ForeignKey('dynamic_rules.Rule')
    trigger_content_type = models.ForeignKey('contenttypes.ContentType')
    trigger_model_id = models.PositiveIntegerField(db_index=True)
    trigger_model = generic.GenericForeignKey(fk_field='trigger_model_id',
                                              ct_field='trigger_content_type')

    The trigger_model represents the model that the Rule inspects to
    determine what "dynamic action" to take.

    The silent_indicator represents a truthy or falsie variable that will
    be used to include a filter to remove violations with a silent == True.
    """

    def get_by_trigger_model(self, trigger_model, silent_indicator=None):
        trigger_content_type = ContentType.objects.get_for_model(trigger_model)
        search_args = dict(trigger_content_type=trigger_content_type, trigger_model_id=trigger_model.pk)
        if silent_indicator:
            search_args['silent'] = False
        return self.filter(**search_args)

    def get_by_rule(self, rule, trigger_model, silent_indicator=None):
        base_query = self.get_by_trigger_model(trigger_model, silent_indicator)
        return base_query.filter(rule=rule)
