
import mock

from django.utils import unittest
from django import forms

from djadmin_ext.admin_forms import BaseAjaxModelForm

from dynamic_rules import admin_forms, models, rule_registry


__all__ = ('AdminRuleFormTests', )

class RuleOne(object):
    fields = {
        'field_one': forms.IntegerField(),
    }
    key = "rule_one"
    display_name = "Rule One"

class RuleTwo(object):
    key = "rule_two"
    display_name = "Rule Two"

    fields = {
        'field_two': forms.CharField(),
        'field_three': forms.CharField(),
    }

class RuleThree(object):
    key = "rule_three"
    display_name = "Rule Three"
    fields = {}

    @classmethod
    def customize_form(cls, form):
        cls.do_customizations(form)

    do_customizations = None # mock

class AdminRuleFormTests(unittest.TestCase):

    def setUp(self):
        self._test_rule_classes = [RuleOne, RuleTwo, RuleThree]
        self._original_rules = [r for r in rule_registry.values()]

        self._unregister_rules(*self._original_rules)
        self._register_rules(*self._test_rule_classes)

    def tearDown(self):
        self._unregister_rules(*self._test_rule_classes)
        self._register_rules(*self._original_rules)

    def _unregister_rules(self, *rules):
        _ = [rule_registry.unregister(r) for r in rules]

    def _register_rules(self, *rules):
        _ = [rule_registry.register(r) for r in rules]

    def test_rule_form_is_a_subclass_of_base_ajax_model_form(self):
        self.assertTrue(issubclass(admin_forms.RuleForm, BaseAjaxModelForm))

    def test_sets_ajax_change_field_to_rule(self):
        self.assertEqual('key', admin_forms.RuleForm.ajax_change_field)

    def test_should_be_a_model_form_for_rule_model_and_limit_fields(self):
        self.assertEqual(models.Rule, admin_forms.RuleForm._meta.model)
        self.assertEqual(('name', 'key', 'group_object_id', 'content_type'), admin_forms.RuleForm._meta.fields)

    def test_sets_rule_key_choices_to_registered_rules(self):
        form = admin_forms.RuleForm()
        self.assertItemsEqual([
            ('', '---------'),
            (RuleOne.key, RuleOne.display_name),
            (RuleTwo.key, RuleTwo.display_name),
            (RuleThree.key, RuleThree.display_name),
        ], form.fields['key'].choices)

    def test_return_empty_dict_when_no_rule_in_data_or_initial(self):
        form = admin_forms.RuleForm()
        self.assertEqual({}, form.dynamic_fields)

    def test_returns_dict_of_rule_fields_from_dynamic_fields_property_when_rule_in_data(self):
        form = admin_forms.RuleForm(data={'key':'rule_one'})
        self.assertEqual(RuleOne.fields, form.dynamic_fields)

    def test_returns_dict_of_rule_fields_from_dynamic_fields_property_when_rule_in_initial(self):
        form = admin_forms.RuleForm(initial={'key':'rule_two'})
        self.assertEqual(RuleTwo.fields, form.dynamic_fields)

    def test_data_trumps_initial_when_getting_rule_class_in_dynamic_fields_property(self):
        form = admin_forms.RuleForm(data={'key':'rule_one'}, initial={'key': 'rule_two'})
        self.assertEqual(RuleOne.fields, form.dynamic_fields)

    def test_sets_initial_data_on_form_field_to_matching_saved_instance_dynamic_fields_value(self):
        expected_value = 'value_one'
        instance = models.Rule(pk=1, key="rule_one", dynamic_fields={'field_one': expected_value})
        form = admin_forms.RuleForm(instance=instance)
        self.assertEqual(expected_value, form.fields['field_one'].initial)

    def test_does_not_set_initial_data_on_form_fields_when_no_saved_instance(self):
        instance = models.Rule(key="rule_one", dynamic_fields={'field_one': "value_one"})
        form = admin_forms.RuleForm(instance=instance)
        self.assertEqual(None, form.fields['field_one'].initial)

    def test_sets_instance_dynamic_fields_to_dict_of_cleaned_data_dynamic_field_values(self):
        dynamic_fields = {'field_two': "value_two", 'field_three': "value_three"}
        form_data = dict(key="rule_two", name="my_rule", **dynamic_fields)

        form = admin_forms.RuleForm(data=form_data)
        form.cleaned_data = form_data

        form_dynamic_data = form._get_dynamic_data_for_instance()
        self.assertEqual(dynamic_fields, form_dynamic_data)

    @mock.patch.object(RuleThree, "do_customizations")
    def test_verify_hook_from_setup_is_called_when_form_is_created_with_data(self, customize_form):
        form_data = dict(key="rule_three")
        form = admin_forms.RuleForm(data=form_data)
        customize_form.assert_called_once_with(form)

    @mock.patch.object(RuleThree, "do_customizations")
    def test_verify_hook_from_setup_is_called_when_form_is_created_with_init(self, customize_form):
        init_form = dict(key="rule_three")
        form = admin_forms.RuleForm(initial=init_form)
        customize_form.assert_called_once_with(form)

    @mock.patch.object(RuleThree, "do_customizations")
    def test_does_not_call_customize_form_when_key_is_not_available(self, customize_form):
        admin_forms.RuleForm()

        self.assertFalse(customize_form.called)

    def test_does_not_call_customize_form_when_rule_does_not_define_it(self):
        form_data = dict(key="rule_one")

        try:
            admin_forms.RuleForm(data=form_data)
        except AttributeError:
            self.fail("should not have raised an Attribute Error")

    @mock.patch('dynamic_rules.admin_forms.RuleForm._get_dynamic_data_for_instance')
    def test_sets_dynamic_fields_on_model_and_returns_model_in_save(self, _get_dynamic_data_for_instance):
        form = admin_forms.RuleForm()
        model_instance = mock.Mock(spec_set=models.Rule)

        with mock.patch('django.forms.ModelForm.save') as modelform_save:
            modelform_save.return_value = model_instance
            saved_model = form.save(commit=False)

        self.assertEqual(model_instance.dynamic_fields, _get_dynamic_data_for_instance.return_value)
        self.assertEqual(model_instance, saved_model)

    def test_calls_save_on_base_model_form_with_instance_and_commit_equals_false(self):
        form = admin_forms.RuleForm()
        model_instance = mock.Mock(spec_set=models.Rule)

        with mock.patch('django.forms.ModelForm.save') as modelform_save:
            modelform_save.return_value = model_instance
            form.save(commit=False)

        modelform_save.assert_called_once_with(form, False)
        self.assertFalse(model_instance.save.called)

    def test_saves_model_when_commit_is_true(self):
        model_instance = mock.Mock(spec_set=models.Rule)
        form = admin_forms.RuleForm()

        with mock.patch('django.forms.ModelForm.save') as modelform_save:
            modelform_save.return_value = model_instance
            form.save()

        modelform_save.assert_called_once_with(form, False)
        model_instance.save.assert_called_once_with()
