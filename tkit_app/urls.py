from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from tkit_app import views
from django_messages import views as dmv

urlpatterns = patterns('',
    # Static pages
    url(r'^dashboard/$', TemplateView.as_view(template_name="base.html")),
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),
    url(r'^documentation/dev/$', TemplateView.as_view(template_name="doc-dev.html")),
    url(r'^documentation/users/$', TemplateView.as_view(template_name="doc-users.html")),

    # TODO
    url(r'^lockscreen/$', TemplateView.as_view(template_name="lockscreen.html")),

    # Sign up
    url(r'^signup/$', views.register),
    url(r'^signup-success/$', TemplateView.as_view(template_name="registration/signup_success.html")),
    #url(r'^disable-account/$', views),

    # Login - Logout
    url(r'^$', login),
    url(r'^login/$', login),
    url(r'^logout/$', logout, {'next_page': '/'}),

    # Classes
    url(r'^classes/$', views.classes),
    url(r'^classes/add/$', views.add_class),
    url(r'^classes/remove/(?P<id_class>\d+)/$', views.remove_class),
    url(r'^classes/(?P<id_class>\d+)/report/$', views.class_report),

    # TODO
    url(r'^classes/(?P<id_class>\d+)/modify/$', views.mod_class),

    # Students
    url(r'^classes/(?P<id_class>\d+)/students/$', views.students),
    url(r'^classes/(?P<id_class>\d+)/students/add/$', views.add_student),
    url(r'^classes/(?P<id_class>\d+)/students/remove/(?P<id_student>\d+)/$', views.remove_student),

    # TODO
    url(r'^classes/(?P<id_class>\d+)/students/modify/(?P<id_student>\d+)/$', views.mod_student),

    url(r'^students/(?P<id_student>\d+)/grades-chart/$', views.grades_chart),

    # TODO
    url(r'^students/(?P<id_student>\d+)/grades-performance-chart/', views.grades_performance_chart),

    url(r'^students/(?P<id_student>\d+)/notes-chart/', views.notes_chart),
    url(r'^students/(?P<id_student>\d+)/attendance-chart/', views.attendance_chart),
    url(r'^students/(?P<id_student>\d+)/$', views.student_info),
    url(r'^students/(?P<id_student>\d+)/notes/add/', views.add_note),

    # Gradebook
    url(r'^classes/(?P<id_class>\d+)/gradebook/$', views.grade_book),
    url(r'^classes/(?P<id_class>\d+)/gradebook/add/$', views.add_gradable_item),
    url(r'^gradebook/update/'
        r'(?P<id_grade>\d+)/(?P<grade>[\w|\W]+)/$', views.update_grade),

    # Attendance
    url(r'^classes/(?P<id_class>\d+)/attendance/(?P<date>[\w|\W]+)/$', views.attendance),
    url(r'^attendance/update/(?P<id_att>\d+)/(?P<att_type>[\w|\W]+)/$', views.update_attendance_type),

    # Lessons
    url(r'^lessons/$', views.lessons),
    url(r'^lessons/add/$', views.add_lesson),
    url(r'^lessons/remove/(?P<id_lesson>[\w|\W]+)/$', views.remove_lesson),

    # Homework
    url(r'^classes/(?P<id_class>\d+)/homework/$', views.homework),
    url(r'^classes/(?P<id_class>\d+)/homework/add/$', views.add_assignment),
    url(r'^classes/(?P<id_class>\d+)/homework/remove/(?P<id_assignment>\d+)/$', views.remove_assignment),

    # To do list
    url(r'^todolist/', views.to_do_list),
    url(r'^todolist/add/$', views.add_todolist_item),
    url(r'^todolist/remove/(?P<id_item>[\w|\W]+)/$', views.remove_lesson),

    # Mailbox entry
    url(r'^mailbox/inbox/', views.mailbox_inbox),
    url(r'^mailbox/outbox/', views.mailbox_outbox),
    url(r'^mailbox/trash/', views.mailbox_trash),
    url(r'^mailbox/compose/', dmv.compose, {'template_name': 'mailbox_compose.html', 'success_url': '/mailbox/inbox/'}),
    url(r'^mailbox/view/(?P<message_id>[\d]+)/$', dmv.view, {'template_name': 'mailbox_view.html'}),
    url(r'^mailbox/reply/(?P<message_id>[\d]+)/', dmv.reply, {'template_name': 'mailbox_compose.html',
                                                              'success_url': '/mailbox/inbox/'})
)