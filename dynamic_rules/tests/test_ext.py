from django.utils import unittest
from django.contrib.contenttypes.models import ContentType

import mock

from dynamic_rules import ext, models

class RuleExtensionManagerTests(unittest.TestCase):

    def setUp(self):
        self.trigger_model = mock.Mock()

    @mock.patch.object(ContentType.objects, 'get_for_model')
    def test_get_content_type_for_model_in_get_by_trigger_model(self, get_for_model):
        manager = mock.Mock(spec_set=ext.RuleExtensionManager)
        ext.RuleExtensionManager.get_by_trigger_model(manager, self.trigger_model)
        get_for_model.assert_called_once_with(self.trigger_model)

    @mock.patch.object(ContentType.objects, 'get_for_model')
    def test_get_by_trigger_model_returns_rules_for_related_object(self, get_for_model):
        manager = mock.Mock(spec_set=ext.RuleExtensionManager)
        violations = ext.RuleExtensionManager.get_by_trigger_model(manager, self.trigger_model)

        manager.filter.assert_called_once_with(
            trigger_content_type=get_for_model.return_value,
            trigger_model_id=self.trigger_model.pk,
        )
        self.assertEqual(manager.filter.return_value, violations)

    def test_violations_queries_on_validation_object_and_rule_model(self):
        rule = models.Rule(pk=1)
        manager = mock.Mock(spec_set=ext.RuleExtensionManager)

        violations = ext.RuleExtensionManager.get_by_rule(manager, rule, self.trigger_model)
        manager.get_by_trigger_model.assert_called_once_with(self.trigger_model)
        base_query = manager.get_by_trigger_model.return_value
        base_query.filter.assert_called_once_with(rule=rule)
        self.assertEqual(base_query.filter.return_value, violations)