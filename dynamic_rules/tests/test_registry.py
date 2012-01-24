
"""
Todo; remove in a future version. No need to add these
methods anymore, they're only here for backwards compatibility.
"""

from django.utils import unittest

from dynamic_rules import sites


__all__ = ('RegistryTests',)

class RuleOne(object):
    key = "rule_one"

class RegistryTests(unittest.TestCase):

    def setUp(self):
        self.registry = sites.RuleRegistry()
        self.rule = RuleOne
        self.registry.register(self.rule)

    def test_returns_rule_class_for_key_in_get_rule_class(self):
        rule_class = self.registry.get_rule_class(self.rule.key)
        self.assertEqual(self.rule, rule_class)

    def test_returns_all_registered_rules_from_rules_property(self):
        self.assertEqual({self.rule.key: self.rule}, self.registry.rules)

    def test_sites_site_is_registry_instance(self):
        self.assertIsInstance(sites.site, sites.Registry)
