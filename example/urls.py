from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
import dynamic_rules

admin.autodiscover()
dynamic_rules.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
