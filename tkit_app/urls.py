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
    url(r'^classes/remove/(?P<id_class>\d+)/$', views.remove_class),

    # Students
    url(r'^classes/(?P<class_name>[\w|\W]+)/students/$', views.students),
    url(r'^classes/(?P<class_name>[\w|\W]+)/students/add/$', views.add_student),
    url(r'^classes/(?P<class_name>[\w|\W]+)/students/remove/(?P<id_student>[\w|\W]+)/$', views.remove_student),
    url(r'^students/(?P<id_student>\d+)/grades-chart/$', views.grades_chart),
    url(r'^students/(?P<id_student>[\w|\W]+)/$', views.student_info),

    # Gradebook
    url(r'^classes/(?P<class_name>[\w|\W]+)/gradebook/$', views.grade_book),
    url(r'^classes/(?P<class_name>[\w|\W]+)/gradebook/add/$', views.add_gradable_item),
    url(r'^gradebook/update/'
        r'(?P<id_grade>[\w|\W]+)/(?P<grade>[\w|\W]+)/$', views.update_grade),

    # Attendance
    url(r'^classes/(?P<class_name>[\w|\W]+)/attendance/$', views.attendance),

    # Lessons
    url(r'^lessons/$', views.lessons),
    url(r'^lessons/add/$', views.add_lesson),
    url(r'^lessons/remove/(?P<id_lesson>[\w|\W]+)/$', views.remove_lesson),

    # Homework
    url(r'^classes/(?P<id_class>\d+)/homework/', views.homework),
    url(r'^classes/(?P<id_class>\d+)/homework/add/$', views.add_homework),
    url(r'^classes/(?P<id_class>\d+)/homework/remove/(?P<id_homework>\d+)/', views.remove_homework),
)