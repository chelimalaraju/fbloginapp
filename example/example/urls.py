from django.conf.urls import patterns, include, url

from django.contrib import admin
from ex.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^done/$', done),
    url(r'^logout_view/$', logout_view),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
)
