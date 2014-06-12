# import os
# from django.conf import settings
# from django.core.files import File
import json
import datetime
from base64 import b64decode
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.core import serializers
from django.db.models import Avg, Count
from django.core.files.base import ContentFile
from django.template import RequestContext
from django.views.generic import FormView, ListView
from django_messages.models import *
from easy_pdf.views import PDFTemplateView
from forms import *
from models import *


def ajax_resp(message):
    """
    Returns an ajax response with the specified message
    """
    tm = datetime.datetime.now().time()

    j = json.dumps({
        "success": True,
        "message": message,
        "time": str(tm.hour) + ":" + str(tm.minute) + ":" + str(tm.second)
    })
    return HttpResponse(content=j, content_type="application/json")


def register(request):
    """
    View for registration form and saving
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()

    return render(request, 'registration/register.html', args)


def disable_account(request):
    u = request.user
    u.is_active = False


def disable_lockscreen(request, pwd):
    """
    View for lockscreen feature.
    If the password is correct return 'yes' otherwise 'no'
    """
    return ajax_resp("yes") if request.user.check_password(pwd) else ajax_resp("no")


class ClassesList(ListView):
    """
    Generic class-based view for listing the classes
    of the current teacher.
    """
    context_object_name = 'classes'
    template_name = 'classes.html'

    def get_queryset(self):
        return Classes.objects.filter(teacher=self.request.user)


def add_class(request, id_class=None):
    """
    View for adding or updating a class:
    it depends on the id_class parameter.
    """
    if request.method == "POST":
        form = AddClassForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            cl_name = form.cleaned_data["name"]
            school = form.cleaned_data["school"]
            desc = form.cleaned_data["description"]

            # Save class into db
            cl = Classes(id=id_class, name=cl_name, school=school, description=desc, teacher=request.user)
            cl.save()

    return redirect('/classes/')


def remove_class(request, id_class):
    """
    View for removing a specified class
    """
    c = Classes.objects.get(pk=id_class)
    c.delete()

    return redirect("/classes/")


def class_report(request, id_class):
    # Students
    cl = Classes.objects.get(pk=id_class)
    stds = Students.objects.filter(s_class=cl)

    # Number of students
    nums = len(stds)

    # Average for every test
    # gds = Grades.objects.filter(student__in=[s for s in stds])
    avg_grades = Grades.objects.filter(student__in=[s for s in stds]).values('subject').distinct()\
        .annotate(avg_grades=Avg('grade'))

    # For every student get the number of absence
    abs_per_std = Attendance.objects.filter(student__in=[s for s in stds], type="Assente")\
        .values('student_id', 'student__first_name', 'student__last_name').distinct().annotate(absence=Count('type'))

    # For every student get the number of presence
    pr_per_std = Attendance.objects.filter(student__in=[s for s in stds], type="Presente")\
        .values('student_id', 'student__first_name', 'student__last_name').distinct().annotate(presence=Count('type'))

    return render_to_response("class-report.html", {
        "class": cl,
        "students_number": nums,
        "avg_grades": avg_grades,
        "aps": abs_per_std,
        "pps": pr_per_std
    }, context_instance=RequestContext(request))


def class_grades_performance_chart(request, id_class):
    """
    Returns a JSON object in order to plot a Google Chart
    grades performance graph
    """
    avg_grades = Grades.objects.values('date', 'subject').distinct().annotate(avg_grades=Avg('grade'))

    rows = [{"c": [{"v": str(g["date"]), "f": None}, {"v": g["avg_grades"], "f": None}]} for g in avg_grades]

    j = json.dumps({
        "cols": [
            {"id": "", "label": "Data", "pattern": "", "type": "string"},
            {"id": "", "label": "Valutazione", "pattern": "", "type": "number"}
        ],
        "rows": rows
    })
    return HttpResponse(content=j, content_type="application/json")


def students(request, id_class):
    """
    View for listing the students of a specified class
    """
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.all().filter(s_class=cl)

    return render_to_response("students.html", {
        "students": ss,
        "class": cl,
        "nums": len(ss)
    }, context_instance=RequestContext(request))


def add_student(request, id_class, id_student=None):
    """
    View for adding or updating a student in a specified class:
    it depends on the id_student parameter.
    """
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            parent = form.cleaned_data["parent"]
            parent_email = form.cleaned_data["parent_email"]
            photo = request.FILES["photo"] if "photo" in request.FILES else None

            # Save student into db
            c = Classes.objects.get(pk=id_class)
            s = Students(id=id_student, first_name=first_name, last_name=last_name,
                         email=email, parent=parent, parent_email=parent_email, photo=photo, s_class=c)
            s.save()

    return redirect('/classes/' + id_class + '/students/')


def remove_student(request, id_class, id_student):
    """
    View for removing a specified student.
    If the student has attached a photo this will also be removed.
    """
    s = Students.objects.get(pk=id_student)

    # Remove student's photo (if exists)
    if s.photo:
        os.remove(s.photo.path)

    s.delete()

    return redirect("/classes/" + id_class + "/students/")


def student_info(request, id_student):
    """
    View for getting information about a specified student
    """
    student = Students.objects.get(pk=id_student)
    notes = Notes.objects.filter(student=student)
    num_nn_notes = len(Notes.objects.filter(student=student, n_type=False))
    num_abs = len(Attendance.objects.filter(student=student, type="Assente"))

    return render_to_response("student-report.html", {
        "student": student,
        "notes": notes,
        "num_nn_notes": num_nn_notes,
        "num_abs": num_abs
    }, context_instance=RequestContext(request))


class StudentReportPDF(PDFTemplateView):
    """
    Generic class-based view for a PDF report of a particular student
    """
    template_name = "student-report-pdf.html"

    def get_context_data(self, id_student):
        student = Students.objects.get(pk=id_student)
        notes = Notes.objects.filter(student=student)
        grades = Grades.objects.filter(student=student)
        attendance = Attendance.objects.filter(student=student)

        return super(StudentReportPDF, self).get_context_data(
            student=student,
            notes=notes,
            grades=grades,
            attendance=attendance
        )


class ClassReportPDF(PDFTemplateView):
    """
    Generic class-based view for a PDF report of a particular class
    """
    template_name = "class-report-pdf.html"

    def get_context_data(self, id_class):
        cl = Classes.objects.get(pk=id_class)
        stds = Students.objects.filter(s_class=cl)

        # Numero studenti
        nums = len(stds)

        # Media per ogni prova fatta
        # gds = Grades.objects.filter(student__in=[s for s in stds])
        avg_grades = Grades.objects.filter(student__in=[s for s in stds]).values('subject').distinct()\
            .annotate(avg_grades=Avg('grade'))

        # Per ogni alunno il numero totale di assenze
        abs_per_std = Attendance.objects.filter(student__in=[s for s in stds], type="Assente")\
            .values('student_id', 'student__first_name', 'student__last_name').distinct().annotate(absence=Count('type'))

        # Per ogni alunno il numero totale di presenze
        pr_per_std = Attendance.objects.filter(student__in=[s for s in stds], type="Presente")\
            .values('student_id', 'student__first_name', 'student__last_name').distinct().annotate(presence=Count('type'))

        return super(ClassReportPDF, self).get_context_data(
            cl=cl,
            students_number=nums,
            avg_grades=avg_grades,
            aps=abs_per_std,
            pps=pr_per_std
        )


def grades_chart(request, id_student):
    """
    Returns a JSON object in order to plot a Google Chart
    grades graph for the specified student
    """
    student = Students.objects.get(pk=id_student)
    grades = Grades.objects.filter(student=student)
    rows = [{"c": [{"v": g.subject, "f": None}, {"v": g.grade, "f": None}]} for g in grades]

    j = json.dumps({
        "cols": [
            {"id": "", "label": "Subject", "pattern": "", "type": "string"},
            {"id": "", "label": "Grade", "pattern": "", "type": "number"}
        ],
        "rows": rows
    })
    return HttpResponse(content=j, content_type="application/json")


def grades_performance_chart(request, id_student):
    """
    Returns a JSON object in order to plot a Google Chart
    grades performance graph for the specified student
    """
    student = Students.objects.get(pk=id_student)
    grades = Grades.objects.filter(student=student).order_by('date')

    rows = [{"c": [{"v": g.subject, "f": None}, {"v": g.grade, "f": None}]} for g in grades]

    j = json.dumps({
        "cols": [
            {"id": "", "label": "Data", "pattern": "", "type": "string"},
            {"id": "", "label": "Valutazione", "pattern": "", "type": "number"}
        ],
        "rows": rows
    })
    return HttpResponse(content=j, content_type="application/json")


def notes_chart(request, id_student):
    """
    Returns a JSON object in order to plot a Google Chart
    notes graph for the specified student
    """
    student = Students.objects.get(pk=id_student)
    notes = Notes.objects.filter(student=student)
    nnotes = [note.n_type for note in notes]

    j = json.dumps({
        "cols": [
            {"id": "", "label": "Type", "pattern": "", "type": "string"},
            {"id": "", "label": "Frequency", "pattern": "", "type": "number"}
        ],
        "rows": [
            {"c": [{"v": "Positive", "f": None}, {"v": nnotes.count(True), "f": None}]},
            {"c": [{"v": "Negative", "f": None}, {"v": nnotes.count(False), "f": None}]}
        ]
    })
    return HttpResponse(content=j, content_type="application/json")


def add_note(request, id_student):
    """
    View for adding a note (positive or negative)
    to the specified student
    """
    if request.method == "POST":
        form = AddNoteForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            n_type = form.cleaned_data["positive"]
            date = form.cleaned_data["date"]
            comment = form.cleaned_data["comment"]

            # Save student into db
            s = Students.objects.get(pk=id_student)
            n = Notes(n_type=n_type, date=date, comment=comment, student=s)
            n.save()

    return redirect('/students/' + id_student + '/')


def remove_note(request, id_note):
    """
    View for removing the specified note
    """
    n = Notes.objects.get(pk=id_note)
    n.delete()

    return redirect("/students/" + str(n.student.pk) + "/")


def grade_book(request, id_class):
    """
    View that lists all the test of the specified class
    """
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.filter(s_class=cl).values_list('pk', flat=True)
    # Student-grades dictionary
    grades = dict((Students.objects.get(pk=s), Grades.objects.filter(student__pk=s)) for s in ss)
    subs = Grades.objects.values('subject', 'date', 'type').distinct()

    return render_to_response("grade-book.html", {"subs": subs, "class": cl, "grades": grades},
                              context_instance=RequestContext(request))


def add_gradable_item(request, id_class):
    """
    View for adding a gradable item to the students
    of the specified class
    """
    if request.method == "POST":
        form = AddGradableItemForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            subject = form.cleaned_data["subject"]
            date = form.cleaned_data["date"]
            ty = form.cleaned_data["type"]

            # Save gradable item into db
            cl = Classes.objects.get(pk=id_class)
            ss = Students.objects.all().filter(s_class=cl)

            for student in ss:
                g = Grades(subject=subject, date=date, grade=None, type=ty, student=student)
                g.save()

    return redirect('/classes/' + id_class + '/gradebook/')


def update_grade(request, id_grade, grade):
    """
    View for updating a student's grade
    """
    if request.is_ajax():
        g = Grades.objects.get(pk=id_grade)
        g.grade = grade
        g.save()

    return ajax_resp("Grade updated")


def remove_gradable_item(request, id_class, sub_name):
    """
    View for removing a gradable item of the specified class
    """
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.filter(s_class=cl)
    g = Grades.objects.filter(subject=sub_name, student__in=[s for s in ss])
    g.delete()

    return redirect("/classes/" + id_class + "/gradebook/")


def attendance(request, id_class, date):
    """
    View that lists the attendance of the specified class students
    """
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.filter(s_class=cl)
    att = Attendance.objects.filter(student__in=[s for s in ss], date=date)

    if not att:
        for student in ss:
            a = Attendance(date=date, type='NA', student=student)
            a.save()
        att = Attendance.objects.filter(student__in=[s for s in ss], date=date)

    return render_to_response("attendance.html", {"date": date, "att": att, "class": cl},
                              context_instance=RequestContext(request))


def update_attendance_type(request, id_att, att_type):
    if request.is_ajax():
        a = Attendance.objects.get(pk=id_att)
        a.type = att_type
        a.save()

    return ajax_resp("Attendance type updated")


def attendance_chart(request, id_student):
    """
    Returns a JSON object in order to plot a Google Chart
    attendance graph for the specified student
    """
    student = Students.objects.get(pk=id_student)
    atts = Attendance.objects.filter(student=student)
    aatts = [att.type for att in atts]

    j = json.dumps({
        "cols": [
            {"id": "", "label": "Type", "pattern": "", "type": "string"},
            {"id": "", "label": "Frequency", "pattern": "", "type": "number"}
        ],
        "rows": [
            {"c": [{"v": "Presenze", "f": None}, {"v": aatts.count("Presente"), "f": None}]},
            {"c": [{"v": "Assenze", "f": None}, {"v": aatts.count("Assente"), "f": None}]}
        ]
    })
    return HttpResponse(content=j, content_type="application/json")


def lessons(request):
    """
    View that lists the lessons of the current teacher/user
    """
    cls = Lessons.objects.filter(teacher=request.user)
    return render_to_response("lessons.html", {"lessons": cls}, context_instance=RequestContext(request))


def add_lesson(request, id_lesson=None):
    """
    View for adding or updating a lesson:
    it depends on the id_lesson attribute
    """
    if request.method == "POST":
        form = AddLessonForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            date = form.cleaned_data["date"]

            # Save lesson into db
            l = Lessons(id=id_lesson, title=title, description=desc, date=date, teacher=request.user)
            l.save()

    return redirect("/lessons/")


def remove_lesson(request, id_lesson):
    """
    View for removing a lesson
    """
    l = Lessons.objects.get(pk=id_lesson)
    l.delete()

    return redirect("/lessons/")


def lesson_boards(request, id_lesson):
    """
    View for listing the board of the specified lesson
    """
    b_lesson = Lessons.objects.get(pk=id_lesson)
    boards = Boards.objects.filter(lesson=b_lesson)
    return render_to_response("boards.html", {"boards": boards, "lesson": b_lesson}, context_instance=RequestContext(request))


def save_board(request, id_lesson):
    """
    View for saving a board
    """
    if request.is_ajax():
        file_name = request.POST["file_name"]
        fname = file_name if file_name.split('.')[-1] == json else file_name + ".png"

        # Save to database and fs
        _, b64data = request.POST["img_data"].split(',')
        image_data = b64decode(b64data)

        board = Boards()
        board.lesson = Lessons.objects.get(pk=id_lesson)
        board.b_file.save(fname, ContentFile(image_data))

    return ajax_resp("Action performed")


def remove_board(request, id_lesson, id_board):
    """
    View for removing a board and its attached file
    """
    # Get file object
    f = Boards.objects.get(pk=id_board)

    # Delete from file system
    try:
        os.remove(f.b_file.path)
    except IOError:
        pass

    # Delete DB reference to the file
    f.delete()

    return redirect("/lessons/" + id_lesson + "/boards/")


def homework(request, id_class):
    """
    View for listing the specified class' assignments
    """
    cl = Classes.objects.get(pk=id_class)
    assm = Assignments.objects.all().filter(a_class=cl)
    return render_to_response("assignments.html", {"assignments": assm, "class": cl}, context_instance=RequestContext(request))


def add_assignment(request, id_class, id_assignment=None):
    """
    View for adding or updating an assignment for the specified class
    """
    if request.method == "POST":
        form = AddAssignmentForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            begin = form.cleaned_data["date_begin"]
            end = form.cleaned_data["date_end"]

            # Save class into db
            cl = Classes.objects.get(pk=id_class)
            assm = Assignments(id=id_assignment, title=title, description=desc, date_begin=begin,
                               date_end=end, a_class=cl)
            assm.save()

    return redirect('/classes/' + str(id_class) + '/homework/')


def remove_assignment(request, id_class, id_assignment):
    """
    View for removing an assignment
    """
    cl = Classes.objects.get(pk=id_class)
    assm = Assignments.objects.get(pk=id_assignment, a_class=cl)
    assm.delete()

    return redirect("/classes/" + id_class + "/homework/")


def to_do_list(request):
    ls = ToDoList.objects.filter(teacher=request.user).order_by("date_exp").reverse()
    return render_to_response("todolist.html", {"list": ls}, context_instance=RequestContext(request))


def add_todolist_item(request, id_item=None):
    """
    View for adding or updating a "to do list" item
    """
    if request.method == "POST":
        form = AddListItemForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            title = form.cleaned_data["title"]
            date = form.cleaned_data["date_exp"]
            perc = form.cleaned_data["perc"]

            # Save item into db
            ls = ToDoList(id=id_item, title=title, date_exp=date, percentage=perc, teacher=request.user)
            ls.save()

    return redirect("/todolist/")


def remove_todolist_item(request, id_item):
    """
    View for removing the specified "to do list" item
    """
    ls = ToDoList.objects.get(pk=id_item)
    ls.delete()

    return redirect("/todolist/")


def mailbox_inbox(request):
    """
    View for getting the inbox message list
    """
    message_list = Message.objects.inbox_for(request.user)

    return render_to_response("mailbox_inbox.html", {
        'message_list': message_list
    }, context_instance=RequestContext(request))


def mailbox_outbox(request):
    """
    View for getting the outbox message list
    """
    message_list = Message.objects.outbox_for(request.user)
    return render_to_response("mailbox_outbox.html", {
        'message_list': message_list,
    }, context_instance=RequestContext(request))


def mailbox_trash(request):
    """
    View for getting the trash message list
    """
    message_list = Message.objects.trash_for(request.user)
    return render_to_response("mailbox_trash.html", {
        'message_list': message_list,
    }, context_instance=RequestContext(request))


def update_color_schema(request, cls):
    """
    View for updating the color schema of the application
    """
    if request.is_ajax():
        try:
            clr = Settings.objects.get(teacher=request.user)
            clr.color_scheme = cls
            clr.save()
        except Exception:
            clr = Settings(color_scheme=cls, teacher=request.user)
            clr.save()

    return ajax_resp("Color schema updated")


def update_absence_limit(request, limit):
    if request.is_ajax():
        try:
            lm = Settings.objects.get(teacher=request.user)
            lm.absence_limit = limit
            lm.save()
        except Exception:
            lm = Settings(absence_limit=limit, teacher=request.user)
            lm.save()

    return ajax_resp("Absence limit updated")


def update_spc_limit(request, limit):
    if request.is_ajax():
        try:
            lm = Settings.objects.get(teacher=request.user)
            lm.spc_limit = limit
            lm.save()
        except Exception:
            lm = Settings(spc_limit=limit, teacher=request.user)
            lm.save()

    return ajax_resp("SPC limit updated")


def update_negative_notes_limit(request, limit):
    if request.is_ajax():
        try:
            lm = Settings.objects.get(teacher=request.user)
            lm.negative_notes_limit = limit
            lm.save()
        except Exception:
            lm = Settings(negative_notes_limit=limit, teacher=request.user)
            lm.save()

    return ajax_resp("NN limit updated")


def update_settings(request, abs_limit, nn_limit, spc_limit):
    update_absence_limit(request, abs_limit)
    update_negative_notes_limit(request, nn_limit)
    update_spc_limit(request, spc_limit)

    return ajax_resp("Settings updated")


def mind_map(request):
    """
    View for listing the pre-saved mind maps
    """
    mmaps = MindMap.objects.all().filter(teacher=request.user)
    return render_to_response("mindmap.html", {"mindmaps": mmaps}, context_instance=RequestContext(request))


def save_mind_map(request):
    """
    View for saving a created mind map with its file
    """
    if request.is_ajax():
        file_name = request.POST["file_name"]
        fname = file_name if file_name.split('.')[-1] == json else file_name + ".json"

        # Save to database and fs
        mm_file = MindMap()
        mm_file.teacher = request.user
        mm_file.json_file.save(fname, ContentFile(request.POST["json_data"]))

    return ajax_resp("Action performed")


def load_mind_map(request, id_map):
    """
    View for loading the specified mind map
    """
    mmap = MindMap.objects.get(pk=id_map)
    data = mmap.json_file.read()
    return ajax_resp(data)


def remove_mind_map(request, id_map):
    """
    View for removing the specified mind map and its attached JSON file
    """
    # Get file object
    f = MindMap.objects.get(pk=id_map)

    # Delete from file system
    try:
        os.remove(f.json_file.path)
    except IOError:
        pass

    # Delete DB reference to the file
    f.delete()

    return redirect("/mindmap/")


class MindMapView(FormView):
    template_name = "mindmap_form.html"
    form_class = MindMapForm

    def form_valid(self, form):
        json_file = MindMap(json_file=self.get_form_kwargs().get("files")["json_file"], teacher=self.request.user)
        json_file.save()
        self.id = json_file.id

        return redirect("/mindmap/")


def presentation_tool(request):
    """
    View for listing the pre-saved presentations
    """
    ps = Presentation.objects.filter(teacher=request.user)
    return render_to_response("presentation.html", {"pres": ps}, context_instance=RequestContext(request))


def save_pres(request, id_pres=None):
    """
    View for saving a new or a pre-saved presentation
    """
    if request.is_ajax():
        if id_pres is None:
            file_name = request.POST["file_name"]
            fname = file_name if file_name.split('.')[-1] == json else file_name + ".html"

            # Save to database and fs
            pres = Presentation()
            pres.title = request.POST["title"]
            pres.description = request.POST["description"]
            pres.teacher = request.user
            pres.pres_file.save(fname, ContentFile(request.POST["html_data"]))
        else:
            pres = Presentation.objects.get(pk=id_pres)
            pres.title = request.POST["title"]
            pres.description = request.POST["description"]

            if os.path.exists(pres.pres_file.path):
                os.remove(pres.pres_file.path)

            pres.pres_file.save(os.path.basename(pres.pres_file.name), ContentFile(request.POST["html_data"]))
            pres.save()

    return ajax_resp("Action performed")


def load_pres(request, id_pres):
    """
    View for loading a pre-saved presentation
    """
    pres = Presentation.objects.get(pk=id_pres)
    data = pres.pres_file.read()

    return render_to_response("presentation-create.html", {
        "data": data,
        "pres": pres
    }, context_instance=RequestContext(request))


def remove_pres(request, id_pres):
    """
    View for removing a presentation and its HTML file
    """
    # Get file object
    f = Presentation.objects.get(pk=id_pres)

    # Delete from file system
    try:
        os.remove(f.pres_file.path)
    except IOError:
        pass

    # Delete DB reference to the file
    f.delete()

    return redirect("/presentation/")


def doc_editor(request):
    """
    View for listing the pre-saved documents
    """
    docs = Document.objects.filter(teacher=request.user)
    return render_to_response("editor.html", {"docs": docs}, context_instance=RequestContext(request))


def save_doc(request):
    """
    View for saving a new document
    """
    if request.is_ajax():
        file_name = request.POST["file_name"]
        fname = file_name if file_name.split('.')[-1] == json else file_name + ".html"

        # Save to database and fs
        doc = Document()
        doc.teacher = request.user
        doc.doc_file.save(fname, ContentFile(request.POST["html_data"]))

    return ajax_resp("Action performed")


def load_doc(request, id_doc):
    """
    View for loading the specified document
    """
    doc = Document.objects.get(pk=id_doc)
    data = doc.doc_file.read()
    return ajax_resp(data)


def remove_doc(request, id_doc):
    """
    View for removing the specified document and its file
    """
    # Get file object
    f = Document.objects.get(pk=id_doc)

    # Delete from file system
    try:
        os.remove(f.doc_file.path)
    except IOError:
        pass

    # Delete DB reference to the file
    f.delete()

    return redirect("/editor/")


def papers(request):
    """
    View for listing the pre-saved papers
    """
    pps = Papers.objects.filter(teacher=request.user)
    return render_to_response("papers.html", {"papers": pps}, context_instance=RequestContext(request))


def add_paper(request):
    """
    View for adding a paper
    """
    if request.method == "POST":
        form = AddPaperForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            title = form.cleaned_data["title"]
            abstract = form.cleaned_data["abstract"]
            p_file = request.FILES["p_file"] if "p_file" in request.FILES else None

            # Save paper into db
            p = Papers(paper_file=p_file, title=title, abstract=abstract, teacher=request.user)
            p.save()

    return redirect('/papers/')


def remove_paper(request, id_paper):
    """
    View for removing the specified paper
    """
    p = Papers.objects.get(pk=id_paper)
    if p.paper_file:
        os.remove(p.paper_file.path)
    p.delete()

    return redirect("/papers/")


def calendar(request):
    """
    View for visualizing on the Javascript calendar tool the current user's events
    """
    todos = ToDoList.objects.filter(teacher=request.user)
    ls = Lessons.objects.filter(teacher=request.user)
    assignments = Assignments.objects.filter(a_class__teacher=request.user)

    return render_to_response("calendar.html", {
        "todos": serializers.serialize('json', todos, fields=('title', 'date_exp')),
        "lessons": serializers.serialize('json', ls, fields=('title', 'date')),
        "assignments": serializers.serialize('json', assignments, fields=('title', 'date_end')),
    }, context_instance=RequestContext(request))