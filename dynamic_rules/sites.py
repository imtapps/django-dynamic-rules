
__all__ = ('site',)

class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class Registry(object):

    def __init__(self):
        self._registry = {}
        
    def register(self, rule_class):
        if rule_class.key in self._registry:
            err_msg = "Rule key %s has already been registered as %s." % (rule_class.key, self._registry[rule_class.key])
            raise AlreadyRegistered(err_msg)

        self._registry[rule_class.key] = rule_class

        return rule_class

    def unregister(self, rule_class):
        self._registry.pop(rule_class.key, None)

    def get_rule_class(self, key):
        if key not in self._registry:
            raise NotRegistered("Rule key %s has not been registered." % key)
        return self._registry[key]

    @property
    def rules(self):
        return self._registry

site = Registry()

        