from django.db import models

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True, max_length=50)

    def __unicode__(self):
        return u"Customer: %d" % self.customer_id
    
class ModelToCheck(models.Model):
    customer = models.ForeignKey('Customer')
    value = models.IntegerField()
    
