from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from sigil import views
from django_messages import views as dmv
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Static pages
    url(r'^$', TemplateView.as_view(template_name="info.html")),
    url(r'^dashboard/$', login_required(TemplateView.as_view(template_name="base.html"), login_url="/login/")),
    url(r'^documentation/developers/$', TemplateView.as_view(template_name="doc-dev.html")),
    url(r'^documentation/users/$', TemplateView.as_view(template_name="doc-users.html")),
    url(r'^lockscreen/$', login_required(TemplateView.as_view(template_name="lockscreen.html"), login_url="/login/")),
    url(r'^lockscreen/disable/(?P<pwd>[\w|\W]+)/$', views.disable_lockscreen),

    # Settings
    url(r'^settings/skin/(?P<cls>[\w|\W]+)/$', views.update_color_schema),
    url(r'^settings/absence-limit/(?P<limit>\d+)/$', views.update_absence_limit),
    url(r'^settings/spc-limit/(?P<limit>\d+)/$', views.update_spc_limit),
    url(r'^settings/nn-limit/(?P<limit>\d+)/$', views.update_negative_notes_limit),
    url(r'^settings/update/(?P<abs_limit>\d+)/(?P<nn_limit>\d+)/(?P<spc_limit>\d+)/$', views.update_settings),

    # Sign up
    url(r'^signup/$', views.register),
    url(r'^signup-success/$', TemplateView.as_view(template_name="registration/signup_success.html")),
    #url(r'^disable-account/$', views),

    # Login - Logout
    url(r'^login/$', login),
    url(r'^logout/$', logout, {'next_page': '/'}),

    # Classes
    url(r'^classes/$', views.ClassesList.as_view()),
    url(r'^classes/add/$', views.add_class),
    url(r'^classes/update/(?P<id_class>\d+)/$', views.add_class),
    url(r'^classes/remove/(?P<id_class>\d+)/$', views.remove_class),
    url(r'^classes/(?P<id_class>\d+)/report/grades-performance-chart/$', views.class_grades_performance_chart),
    url(r'^classes/(?P<id_class>\d+)/report/$', views.class_report),
    url(r'^classes/(?P<id_class>\d+)/report/pdf/$', views.ClassReportPDF.as_view()),

    # Students
    url(r'^classes/(?P<id_class>\d+)/students/$', views.students),
    url(r'^classes/(?P<id_class>\d+)/students/add/$', views.add_student),
    url(r'^classes/(?P<id_class>\d+)/students/update/(?P<id_student>\d+)/$', views.add_student),
    url(r'^classes/(?P<id_class>\d+)/students/remove/(?P<id_student>\d+)/$', views.remove_student),
    url(r'^students/(?P<id_student>\d+)/grades-chart/$', views.grades_chart),
    url(r'^students/(?P<id_student>\d+)/grades-performance-chart/$', views.grades_performance_chart),
    url(r'^students/(?P<id_student>\d+)/notes-chart/$', views.notes_chart),
    url(r'^students/(?P<id_student>\d+)/attendance-chart/$', views.attendance_chart),
    url(r'^students/(?P<id_student>\d+)/$', views.student_info),
    url(r'^students/(?P<id_student>\d+)/pdf/$', views.StudentReportPDF.as_view()),
    url(r'^students/(?P<id_student>\d+)/notes/add/$', views.add_note),
    url(r'^notes/remove/(?P<id_note>\d+)/$', views.remove_note),

    # Gradebook
    url(r'^classes/(?P<id_class>\d+)/gradebook/$', views.grade_book),
    url(r'^classes/(?P<id_class>\d+)/gradebook/add/$', views.add_gradable_item),
    url(r'^classes/(?P<id_class>\d+)/gradebook/remove/(?P<sub_name>[\w|\W]+)/$', views.remove_gradable_item),
    url(r'^gradebook/update/'
        r'(?P<id_grade>\d+)/(?P<grade>[\w|\W]+)/$', views.update_grade),

    # Attendance
    url(r'^classes/(?P<id_class>\d+)/attendance/(?P<date>[\w|\W]+)/$', views.attendance),
    url(r'^attendance/update/(?P<id_att>\d+)/(?P<att_type>[\w|\W]+)/$', views.update_attendance_type),

    # Lessons
    url(r'^lessons/$', views.lessons),
    url(r'^lessons/add/$', views.add_lesson),
    url(r'^lessons/update/(?P<id_lesson>\d+)/$', views.add_lesson),
    url(r'^lessons/remove/(?P<id_lesson>\d+)/$', views.remove_lesson),
    url(r'^lessons/(?P<id_lesson>\d+)/boards/$', views.lesson_boards),
    url(r'^lessons/(?P<id_lesson>\d+)/boards/save/$', views.save_board),
    url(r'^lessons/(?P<id_lesson>\d+)/boards/remove/(?P<id_board>[\d]+)/$', views.remove_board),

    # Homework
    url(r'^classes/(?P<id_class>\d+)/homework/$', views.homework),
    url(r'^classes/(?P<id_class>\d+)/homework/add/$', views.add_assignment),
    url(r'^classes/(?P<id_class>\d+)/homework/update/(?P<id_assignment>\d+)/$', views.add_assignment),
    url(r'^classes/(?P<id_class>\d+)/homework/remove/(?P<id_assignment>\d+)/$', views.remove_assignment),

    # To do list
    url(r'^todolist/$', views.to_do_list),
    url(r'^todolist/add/$', views.add_todolist_item),
    url(r'^todolist/update/(?P<id_item>\d+)/$', views.add_todolist_item),
    url(r'^todolist/remove/(?P<id_item>\d+)/$', views.remove_todolist_item),

    # Mailbox entry
    url(r'^mailbox/inbox/$', views.mailbox_inbox),
    url(r'^mailbox/outbox/$', views.mailbox_outbox),
    url(r'^mailbox/trash/$', views.mailbox_trash),
    url(r'^mailbox/compose/$', dmv.compose, {
        'template_name': 'mailbox_compose.html', 'success_url': '/mailbox/inbox/'
    }),
    url(r'^mailbox/view/(?P<message_id>[\d]+)/$', dmv.view, {'template_name': 'mailbox_view.html'}),
    url(r'^mailbox/reply/(?P<message_id>[\d]+)/$', dmv.reply, {'template_name': 'mailbox_compose.html',
                                                              'success_url': '/mailbox/inbox/'}),

    # Mind map tool
    url(r'^mindmap/$', views.mind_map),
    url(r'^mindmap/save/$', views.save_mind_map),  # Save mind map to personal account
    url(r'^mindmap/upload/$', views.MindMapView.as_view(), name="mindmap_upload"),  # Upload from file system
    url(r'^mindmap/load/(?P<id_map>[\d]+)/$', views.load_mind_map),  # Load from personal account
    url(r'^mindmap/remove/(?P<id_map>[\d]+)/$', views.remove_mind_map),

    # Presentation tool
    url(r'^presentation/$', views.presentation_tool),
    url(r'^presentation/create/$', login_required(TemplateView.as_view(template_name="presentation-create.html"),
                                                  login_url="/login/")),
    url(r'^presentation/load/(?P<id_pres>[\d]+)/$', views.load_pres),
    url(r'^presentation/save/$', views.save_pres),
    url(r'^presentation/save/(?P<id_pres>[\d]+)/$', views.save_pres),
    url(r'^presentation/remove/(?P<id_pres>[\d]+)/$', views.remove_pres),

    url(r'^editor/$', views.doc_editor),
    url(r'^editor/save/$', views.save_doc),
    url(r'^editor/load/(?P<id_doc>[\d]+)/', views.load_doc),
    url(r'^editor/remove/(?P<id_doc>[\d]+)/$', views.remove_doc),

    # Books
    url(r'^books/$', login_required(TemplateView.as_view(template_name="books.html"), login_url="/login/")),

    # Papers
    url(r'^papers/$', views.papers),
    url(r'^papers/add/$', views.add_paper),
    url(r'^papers/remove/(?P<id_paper>\d+)/$', views.remove_paper),

    # Calendar
    url(r'calendar/$', views.calendar)
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)