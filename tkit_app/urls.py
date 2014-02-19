from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from tkit_app import views

urlpatterns = patterns('',
    # Static pages
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),

    # Sign up
    url(r'^signup/$', views.register),
    url(r'^signup-success/$', TemplateView.as_view(template_name="signup_success.html")),

    # Login - Logout
    url(r'^login/$', login),
    url(r'^logout/$', logout),

    url(r'^classes/$', views.classes),
    url(r'^classes/(?P<class_name>[a-z])/students/$', views.students),
)