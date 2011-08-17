
import mock
from django.utils.unittest import TestCase

from dynamic_rules.dynamic_actions import BaseDynamicAction

__all__ = (
    'BaseDynamicActionTests',
)

class BaseDynamicActionTests(TestCase):

    def setUp(self):
        self.rule_model = mock.Mock()
        self.trigger_model = mock.Mock()

    def test_sets_rule_model_and_trigger_model_on_action_instance(self):
        action = BaseDynamicAction(self.rule_model, self.trigger_model)
        self.assertEqual(self.rule_model, action.rule_model)
        self.assertEqual(self.trigger_model, action.trigger_model)

    def test_sets_trigger_model_name_attribute_on_action_instance_when_present(self):
        class TestAction(BaseDynamicAction):
            trigger_model_name = "my_model"

        action = TestAction(self.rule_model, self.trigger_model)
        self.assertEqual(action.trigger_model, action.my_model)
