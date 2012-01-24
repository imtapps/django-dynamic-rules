
from django import db
from django import forms
from django.dispatch import receiver

from dynamic_rules import rule_registry, models
from dynamic_rules.dynamic_actions import BaseDynamicAction

from sample.models import ModelToCheck

@rule_registry.register
class SampleRuleOne(BaseDynamicAction):
    key = "SampleRuleOne"
    display_name = "Warn when the value is above x"

    fields = {
        'max_value': forms.IntegerField(),
    }

    def run(self, *args, **kwargs):
        if self.trigger_model.value > self.max_value:
            print "\n\nValue must be less than or equal to %d. Your value was %d\n\n" % \
                  (self.max_value, self.trigger_model.value)

@rule_registry.register
class SampleRuleTwo(BaseDynamicAction):
    key = "SampleRuleTwo"
    display_name = "Do something when value is between x and y."

    fields = {
        'x_value': forms.IntegerField(label="Low Value"),
        'y_value': forms.IntegerField(label="High Value"),
    }

    def run(self, *args, **kwargs):
        if not (self.x_value <= self.trigger_model.value <= self.y_value):
            print "\n\nValue must be between %d and %d. Your value was %d\n\n" % \
                  (self.x_value, self.y_value, self.trigger_model.value)

@receiver(db.models.signals.post_save, sender=ModelToCheck, dispatch_uid="check_rules")
def model_post_save(sender, **kwargs):
    instance = kwargs.get('instance')

    rule_models = models.Rule.objects.get_by_group_object(instance.customer)
    for rule_model in rule_models:
        rule_model.run_action(instance)