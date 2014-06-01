from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('sigil.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^admin/', include(admin.site.urls))
)
