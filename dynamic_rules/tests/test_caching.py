from django import test

from dynamic_rules import models as rule_models
from example.sample import models as sample_models


class CachingTests(test.TestCase):

    def test_rules_queries_are_cached(self):
        customer = sample_models.Customer.objects.get(customer_id=1)
        list(rule_models.Rule.objects.get_by_key(customer, 1).all())
        with self.assertNumQueries(0):
            list(rule_models.Rule.objects.get_by_key(customer, 1).all())
