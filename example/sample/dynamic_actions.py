
from django import db
from django import forms
from django.dispatch import receiver

from dynamic_rules import site, models
from dynamic_rules.dynamic_actions import BaseDynamicAction

from sample.models import ModelToCheck

@site.register
class SampleRuleOne(BaseDynamicAction):
    key = "SampleRuleOne"
    display_name = "Warn when the value is above x"

    fields = {
        'max_value': forms.IntegerField(),
    }

    def run(self, *args, **kwargs):
        max_value_allowed = self.rule_model.dynamic_fields.get('max_value', 0)
        if self.trigger_model.value > max_value_allowed:
            print "\n\nValue must be less than or equal to %d. Your value was %d\n\n" % \
                  (max_value_allowed, self.trigger_model.value)

@site.register
class SampleRuleTwo(BaseDynamicAction):
    key = "SampleRuleTwo"
    display_name = "Do something when value is between x and y."

    fields = {
        'x_value': forms.IntegerField(label="Low Value"),
        'y_value': forms.IntegerField(label="High Value"),
    }

    def run(self, *args, **kwargs):
        min_value_allowed = self.rule_model.dynamic_fields.get('x_value', 0)
        max_value_allowed = self.rule_model.dynamic_fields.get('y_value', 0)
        if not (min_value_allowed <= self.trigger_model.value <= max_value_allowed):
            print "\n\nValue must be between %d and %d. Your value was %d\n\n" % \
                  (min_value_allowed, max_value_allowed, self.trigger_model.value)



@receiver(db.models.signals.post_save, sender=ModelToCheck, dispatch_uid="check_rules")
def model_post_save(sender, **kwargs):
    instance = kwargs.get('instance')

    rule_models = models.Rule.objects.get_by_group_object(instance.customer)
    for rule_model in rule_models:
        rule_model.run_action(instance)