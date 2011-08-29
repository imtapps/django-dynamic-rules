
import datetime

import mock
from django.utils.unittest import TestCase
from django import forms

from dynamic_rules.dynamic_actions import BaseDynamicAction

__all__ = (
    'BaseDynamicActionTests',
)

class TestAction(BaseDynamicAction):
    trigger_model_name = "my_model"

    fields = {
        'amount': forms.IntegerField(),
        'start_date': forms.DateField(),
    }

class BaseDynamicActionTests(TestCase):

    def setUp(self):
        self.rule_model = mock.Mock()
        self.trigger_model = mock.Mock()

    def test_sets_rule_model_and_trigger_model_on_action_instance(self):
        action = BaseDynamicAction(self.rule_model, self.trigger_model)
        self.assertEqual(self.rule_model, action.rule_model)
        self.assertEqual(self.trigger_model, action.trigger_model)

    def test_sets_trigger_model_name_attribute_on_action_instance_when_present(self):
        action = TestAction(self.rule_model, self.trigger_model)
        self.assertEqual(action.trigger_model, action.my_model)

    @mock.patch.object(forms.IntegerField, 'to_python')
    def test_action_class_gets_attribute_from_rule_model_dynamic_fields(self, to_python):
        self.rule_model.dynamic_fields = {'amount': '300'}
        action = TestAction(self.rule_model, self.trigger_model)

        amount = action.amount

        to_python.assert_called_once_with('300')
        self.assertEqual(to_python.return_value, amount)

    def test_returns_fields_to_python_value_when_accessing_attribute_on_action(self):
        self.rule_model.dynamic_fields = {'amount': '300', 'start_date': '2011-08-29'}
        action = TestAction(self.rule_model, self.trigger_model)

        self.assertEqual(300, action.amount)
        self.assertEqual(datetime.date(2011, 8, 29), action.start_date)

    def test_rule_model_dynamic_fields_do_not_trump_instance_attributes(self):
        self.rule_model.dynamic_fields = {'some_amount': 500}
        action = TestAction(self.rule_model, self.trigger_model)
        action.some_amount = 1000
        self.assertEqual(1000, action.some_amount)

    def test_raises_attribute_error_when_accessing_attribute_that_doesnt_exist(self):
        action = TestAction(self.rule_model, self.trigger_model)
        with self.assertRaises(AttributeError) as e:
            action.something
        self.assertEqual("'TestAction' object has no attribute 'something'", e.exception.message)

