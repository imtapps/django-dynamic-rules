
from django import db
from django import forms
from django.dispatch import receiver

from dynamic_rules import site, models

from sample.models import ModelToCheck

@site.register
class SampleRuleOne(object):
    key = "SampleRuleOne"
    display_name = "Warn when the value is above x"

    fields = {
        'max_value': forms.IntegerField(),
    }

    def __init__(self, rule_model, model_to_check):
        self.rule_model = rule_model
        self.model_to_check = model_to_check

    def run(self, *args, **kwargs):
        max_value_allowed = self.rule_model.dynamic_fields.get('max_value', 0)
        if self.model_to_check.value > max_value_allowed:
            print "\n\nValue must be less than or equal to %d. Your value was %d\n\n" % \
                  (max_value_allowed, self.model_to_check.value)

@site.register
class SampleRuleTwo(object):
    key = "SampleRuleTwo"
    display_name = "Do something when value is between x and y."

    fields = {
        'x_value': forms.IntegerField(label="Low Value"),
        'y_value': forms.IntegerField(label="High Value"),
    }

    def __init__(self, rule_model, model_to_check):
        self.rule_model = rule_model
        self.model_to_check = model_to_check

    def run(self, *args, **kwargs):
        min_value_allowed = self.rule_model.dynamic_fields.get('x_value', 0)
        max_value_allowed = self.rule_model.dynamic_fields.get('y_value', 0)
        if not (min_value_allowed <= self.model_to_check.value <= max_value_allowed):
            print "\n\nValue must be between %d and %d. Your value was %d\n\n" % \
                  (min_value_allowed, max_value_allowed, self.model_to_check.value)



@receiver(db.models.signals.post_save, sender=ModelToCheck, dispatch_uid="check_rules")
def model_post_save(sender, **kwargs):
    instance = kwargs.get('instance')

    rule_models = models.Rule.objects.get_by_group_object(instance.customer)
    for rule_model in rule_models:
        rule_model.run_action(instance)