
Sometimes when you develop apps for other people, they like to
define their own sets of "rules".

For example, one customer might say the value of a certain field on
a model might be valid when it is between 100 and 1000. Another customer
might consider the same field valid only when the value is between
500 and 1000.

That kind of validation is extremely difficult to do in a modelform's
clean method like you would if you knew beforehand what the valid values
were supposed to be.

This app lets you create some boundaries for various arbitrary parameters
that are tied to some other arbitrary model. Each customer can then define
what the rule parameters will be for their particular organization.


Usage:
First create a file called dynamic_actions.
Inside dynamic actions, you must register your rule class
with the dynamic_rules site.

The rule class must have the following attributes:
  key: a string to identify the rule class with the registry
  display_name: a name to use for the admin_form to show a readable name
  fields: a dictionary of field_names, and django form classes. This declares
          the parameters available.

Additionally, the rule class must accept a rule_model and model_to_check
as initialization arguments, and have a run method that accepts
*args and **kwargs.

To see the dynamic rules in action, syncdb from this project and fire
up the admin. Create a rule tied to group_object_id: 1 (i.e. customer 1)
and content type: 'customer'

Add a ModelToCheck model from the sample app that has a value that
violates your rule. Check the runserver console and see that the
violation printed.

This is best used in conjunction with django-dynamic-validation which lets you
track and store violations to the rules, or django-dynamic-manipulation
which lets you manipulate other data because of a triggered rule.

 - http://pypi.python.org/pypi/django-dynamic-validation
 - http://pypi.python.org/pypi/django-dynamic-manipulation


Recent Updates
--------------
1/24/2012

Updated dynamic_rules to use latest version of django-class-registry (0.0.3)
which handles the registry like a dictionary.

'dynamic_rules.site' should now be referred to as 'dynamic_rule.rule_registry'
however, you can access 'site' for a while. We just believe 'rule_registry'
is a much better name.
