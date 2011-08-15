
from django.contrib import admin

from djadmin_ext.helpers import  BaseAjaxModelAdmin

from dynamic_rules import admin_forms, models

class RuleAdmin(BaseAjaxModelAdmin):
    form = admin_forms.RuleForm
    list_display = ('name', 'group_object')

admin.site.register(models.Rule, RuleAdmin)