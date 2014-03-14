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

    # Classes
    url(r'^classes/$', views.classes),
    url(r'^classes/add/$', views.add_class),
    url(r'^classes/remove/(?P<id_class>[\w|\W]+)/$', views.remove_class),

    # Students
    url(r'^classes/(?P<class_name>[\w|\W]+)/students/$', views.students),
    url(r'^classes/(?P<class_name>[\w|\W]+)/students/add/$', views.add_student),
    url(r'^classes/(?P<class_name>[\w|\W]+)/students/remove/(?P<id_student>\w+)/$', views.remove_student),

    # Gradebook
    url(r'^classes/(?P<class_name>[\w|\W]+)/gradebook/$', views.grade_book),
    url(r'^classes/(?P<class_name>[\w|\W]+)/gradebook/add/$', views.add_gradable_item),

    # Attendance
    url(r'^classes/(?P<class_name>[\w|\W]+)/attendance/$', views.attendance),

    # Lessons
    url(r'^lessons/$', views.lessons),
    url(r'^lessons/add/$', )
)