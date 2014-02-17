from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from tkit_app import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),
    url(r'^classes/$', views.classes),
    url(r'^classes/(?P<class_name>[a-z])/students/$', views.students),
)