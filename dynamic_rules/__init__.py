
from dynamic_rules.sites import site

__all__ = ('site',)

def autodiscover():
    from autoload import autodiscover as discover
    discover("dynamic_actions")