from class_registry.sites import Registry as _Registry

__all__ = ('site',)

class Registry(_Registry):
    get_rule_class = _Registry.get_registered_class
    rules = _Registry.classes

site = Registry()