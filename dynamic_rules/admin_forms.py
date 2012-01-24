from django import forms

from djadmin_ext.admin_forms import BaseAjaxModelForm

from dynamic_rules import models, rule_registry

__all__ = ('RuleForm',)

class RuleForm(BaseAjaxModelForm):
    ajax_change_field = 'key'

    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        rule_choices = [(k, v.display_name) for k, v in rule_registry.items()]
        self.fields['key'] = forms.ChoiceField(choices=[('', '---------')] + rule_choices)

    def setup_dynamic_fields(self):
        super(RuleForm, self).setup_dynamic_fields()
        key = self.get_value_from_data_or_initial('key')

        if key:
            rule_class = rule_registry[key]
            customize_form = getattr(rule_class, 'customize_form', None)
            customize_form(self) if customize_form else None

    @property
    def dynamic_fields(self):
        key = self.get_value_from_data_or_initial('key')
        if key:
            rule_class = rule_registry[key]
            self.set_dynamic_field_initial(rule_class)
            return rule_class.fields
        return {}

    def set_dynamic_field_initial(self, rule_class):
        if self.instance.pk:
            for field_name, field in rule_class.fields.items():
                field.initial = self.instance.dynamic_fields[field_name]

    def _get_dynamic_data_for_instance(self):
        dynamic_data = {}
        for field_name in self.dynamic_fields:
            dynamic_data[field_name] = self.cleaned_data.get(field_name)
        return dynamic_data

    def save(self, commit=True):
        obj = forms.ModelForm.save(self, False)
        obj.dynamic_fields = self._get_dynamic_data_for_instance()
        if commit:
            obj.save()
        return obj

    class Meta(object):
        model = models.Rule
        fields = ('name', 'key', 'group_object_id', 'content_type')