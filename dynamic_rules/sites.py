
import warnings

from class_registry import Registry

__all__ = ('site',)

class RuleRegistry(Registry):

    def get_rule_class(self, key):
        warnings.warn(
            "Don't access this method anymore. Just use the rule_registry as a dictionary",
            PendingDeprecationWarning,
        )
        return self[key]

    @property
    def rules(self):
        warnings.warn(
            "Don't access this method anymore. Just use the rule_registry as a dictionary",
            PendingDeprecationWarning,
        )
        return self

site = RuleRegistry()
