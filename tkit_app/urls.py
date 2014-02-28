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
    url(r'^signup-success/$', TemplateView.as_view(template_name="registration/signup_success.html")),
    #url(r'^disable-account/$', views),

    # Login - Logout
    url(r'^login/$', login),
    url(r'^logout/$', logout, {'next_page': '/'}),

    url(r'^classes/$', views.classes),
    url(r'^classes/add/$', views.add_class),
    url(r'^classes/remove/(?P<id_class>\w+)/$', views.remove_class),
    url(r'^classes/(?P<class_name>\w+)/students/$', views.students),
    url(r'^classes/(?P<class_name>\w+)/students/add/$', views.add_student),
    url(r'^classes/(?P<class_name>\w+)/students/remove/(?P<id_student>\w+)/$', views.remove_student),

    url(r'^classes/(?P<class_name>\w+)/gradebook/$', views.grade_book),
    url(r'^classes/(?P<class_name>\w+)/gradebook/add/$', views.add_gradable_item),
    url(r'^classes/(?P<class_name>\w+)/attendance/$', views.attendance)
)