
class BaseDynamicAction(object):
    trigger_model_name = None

    def __init__(self, rule_model, trigger_model):
        self.rule_model = rule_model
        self.trigger_model = trigger_model

        if self.trigger_model_name:
            setattr(self, self.trigger_model_name, self.trigger_model)

    def __getattr__(self, item):
        if item in self.fields:
            return self.fields[item].to_python(self.rule_model.dynamic_fields[item])
        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, item))

    def run(self, *args, **kwargs):
        """
        Implement this method to actually do something.
        """
        pass