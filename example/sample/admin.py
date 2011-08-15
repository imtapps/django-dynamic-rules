
from django.contrib import admin

from sample import models

class ModelToCheckAdmin(admin.ModelAdmin):
    list_display = ('customer', 'value')

admin.site.register(models.Customer)
admin.site.register(models.ModelToCheck, ModelToCheckAdmin)