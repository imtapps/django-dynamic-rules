
from dynamic_rules.sites import site

# rule_registry is the preferred way to access your registered rules.
# In the future, we will remove the sites file completely and force
# an import from this location.

rule_registry = site

__all__ = ('site', 'rule_registry')

def autodiscover():
    from autoload import autodiscover as discover
    discover("dynamic_actions")