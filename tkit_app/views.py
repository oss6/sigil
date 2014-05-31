import os
import json
import datetime
from base64 import b64decode
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.conf import settings
from django.db.models import Avg, Count
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.generic import FormView
from django_messages.models import *
from easy_pdf.views import PDFTemplateView
from forms import *
from models import *


def ajax_resp(message):
    tm = datetime.datetime.now().time()

    j = json.dumps({
        "success": True,
        "message": message,
        "time": str(tm.hour) + ":" + str(tm.minute) + ":" + str(tm.second)
    })
    return HttpResponse(content=j, content_type="application/json")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()

    return render(request, 'registration/register.html', args)


@login_required(login_url='/login/')
def disable_account(request):
    u = request.user
    u.is_active = False


@login_required(login_url='/login/')
def disable_lockscreen(request, pwd):
    return ajax_resp("yes") if request.user.check_password(pwd) else ajax_resp("no")


@login_required(login_url='/login/')
def classes(request):
    cls = Classes.objects.filter(teacher=request.user)
    return render_to_response("classes.html", {"classes": cls}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_class(request, id_class=None):
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


@login_required(login_url='/login/')
def remove_class(request, id_class):
    c = Classes.objects.get(pk=id_class)
    c.delete()

    return redirect("/classes/")


@login_required(login_url='/login/')
def class_report(request, id_class):
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

    return render_to_response("class-report.html", {
        "class": cl,
        "students_number": nums,
        "avg_grades": avg_grades,
        "aps": abs_per_std,
        "pps": pr_per_std
    }, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def class_grades_performance_chart(request, id_class):
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


@login_required(login_url='/login/')
def students(request, id_class):
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.all().filter(s_class=cl)

    return render_to_response("students.html", {"students": ss, "class": cl, "nums": len(ss)},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_student(request, id_class, id_student=None):
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


@login_required(login_url='/login/')
def remove_student(request, id_class, id_student):
    s = Students.objects.get(pk=id_student)

    # Remove student's photo (if exists)
    if s.photo:
        os.remove(s.photo.path)

    s.delete()

    return redirect("/classes/" + id_class + "/students/")


@login_required(login_url='/login/')
def student_info(request, id_student):
    student = Students.objects.get(pk=id_student)
    notes = Notes.objects.filter(student=student)

    return render_to_response("student-report.html", {
        "student": student,
        "notes": notes
    }, context_instance=RequestContext(request))


class StudentReportPDF(PDFTemplateView):
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


@login_required(login_url='/login/')
def grades_chart(request, id_student):
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


@login_required(login_url='/login/')
def grades_performance_chart(request, id_student):
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


@login_required(login_url='/login/')
def notes_chart(request, id_student):
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


@login_required(login_url='/login/')
def add_note(request, id_student):
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


@login_required(login_url='/login/')
def remove_note(request, id_note):
    n = Notes.objects.get(pk=id_note)
    n.delete()

    return redirect("/students/" + str(n.student.pk) + "/")


@login_required(login_url='/login/')
def grade_book(request, id_class):
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.filter(s_class=cl).values_list('pk', flat=True)
    # Student-grades dictionary
    grades = dict((Students.objects.get(pk=s), Grades.objects.filter(student__pk=s)) for s in ss)
    subs = Grades.objects.values('subject', 'date', 'type').distinct()

    return render_to_response("grade-book.html", {"subs": subs, "class": cl, "grades": grades},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_gradable_item(request, id_class):
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


@login_required(login_url='/login/')
def update_grade(request, id_grade, grade):
    if request.is_ajax():
        g = Grades.objects.get(pk=id_grade)
        g.grade = grade
        g.save()

    return ajax_resp("Grade updated")


@login_required(login_url='/login/')
def remove_gradable_item(request, id_class, sub_name):
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.filter(s_class=cl)
    g = Grades.objects.filter(subject=sub_name, student__in=[s for s in ss])
    g.delete()

    return redirect("/classes/" + id_class + "/gradebook/")


@login_required(login_url='/login/')
def attendance(request, id_class, date):
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


@login_required(login_url='/login/')
def update_attendance_type(request, id_att, att_type):
    if request.is_ajax():
        a = Attendance.objects.get(pk=id_att)
        a.type = att_type
        a.save()

    return ajax_resp("Attendance type updated")


@login_required(login_url='/login/')
def attendance_chart(request, id_student):
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


@login_required(login_url='/login/')
def lessons(request):
    cls = Lessons.objects.filter(teacher=request.user)
    return render_to_response("lessons.html", {"lessons": cls}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_lesson(request, id_lesson=None):
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


@login_required(login_url='/login/')
def remove_lesson(request, id_lesson):
    l = Lessons.objects.get(pk=id_lesson)
    l.delete()

    return redirect("/lessons/")


@login_required(login_url='/login/')
def lesson_boards(request, id_lesson):
    b_lesson = Lessons.objects.get(pk=id_lesson)
    boards = Boards.objects.filter(lesson=b_lesson)
    return render_to_response("boards.html", {"boards": boards, "lesson": b_lesson}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def save_board(request, id_lesson):
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


@login_required(login_url='/login/')
def remove_board(request, id_lesson, id_board):
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


@login_required(login_url='/login/')
def homework(request, id_class):
    cl = Classes.objects.get(pk=id_class)
    assm = Assignments.objects.all().filter(a_class=cl)
    return render_to_response("assignments.html", {"assignments": assm, "class": cl}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_assignment(request, id_class, id_assignment=None):
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


@login_required(login_url='/login/')
def remove_assignment(request, id_class, id_assignment):
    cl = Classes.objects.get(pk=id_class)
    assm = Assignments.objects.get(pk=id_assignment, a_class=cl)
    assm.delete()

    return redirect("/classes/" + id_class + "/homework/")


@login_required(login_url='/login/')
def to_do_list(request):
    ls = ToDoList.objects.filter(teacher=request.user).order_by("date_exp").reverse()
    return render_to_response("todolist.html", {"list": ls}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_todolist_item(request, id_item=None):
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


@login_required(login_url='/login/')
def remove_todolist_item(request, id_item):
    ls = ToDoList.objects.get(pk=id_item)
    ls.delete()

    return redirect("/todolist/")


@login_required(login_url='/login/')
def mailbox_inbox(request):
    message_list = Message.objects.inbox_for(request.user)

    return render_to_response("mailbox_inbox.html", {
        'message_list': message_list
    }, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def mailbox_outbox(request):
    message_list = Message.objects.outbox_for(request.user)
    return render_to_response("mailbox_outbox.html", {
        'message_list': message_list,
    }, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def mailbox_trash(request):
    message_list = Message.objects.trash_for(request.user)
    return render_to_response("mailbox_trash.html", {
        'message_list': message_list,
    }, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def update_color_schema(request, cls):
    if request.is_ajax():
        try:
            clr = Settings.objects.get(teacher=request.user)
            clr.color_scheme = cls
            clr.save()
        except Exception:
            clr = Settings(color_scheme=cls, teacher=request.user)
            clr.save()

    return ajax_resp("Color schema updated")


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def mind_map(request):
    mmaps = MindMap.objects.all().filter(teacher=request.user)
    return render_to_response("mindmap.html", {"mindmaps": mmaps}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def save_mind_map(request):
    if request.is_ajax():
        file_name = request.POST["file_name"]
        fname = file_name if file_name.split('.')[-1] == json else file_name + ".json"

        # Save to database and fs
        mm_file = MindMap()
        mm_file.teacher = request.user
        mm_file.json_file.save(fname, ContentFile(request.POST["json_data"]))

    return ajax_resp("Action performed")


@login_required(login_url='/login/')
def load_mind_map(request, id_map):
    mmap = MindMap.objects.get(pk=id_map)
    data = mmap.json_file.read()
    return ajax_resp(data)


@login_required(login_url='/login/')
def remove_mind_map(request, id_map):
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


@login_required(login_url='/login/')
def presentation_tool(request):
    ps = Presentation.objects.filter(teacher=request.user)
    return render_to_response("presentation.html", {"pres": ps}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def save_pres(request):
    if request.is_ajax():
        file_name = request.POST["file_name"]
        fname = file_name if file_name.split('.')[-1] == json else file_name + ".html"

        # Save to database and fs
        pres = Presentation()
        pres.title = request.POST["title"]
        pres.description = request.POST["description"]
        pres.teacher = request.user
        pres.pres_file.save(fname, ContentFile(request.POST["html_data"]))

    return ajax_resp("Action performed")


@login_required(login_url='/login/')
def load_pres(request, id_pres):
    pass


@login_required(login_url='/login/')
def remove_pres(request, id_pres):
    pass


@login_required(login_url='/login/')
def doc_editor(request):
    docs = Document.objects.filter(teacher=request.user)
    return render_to_response("editor.html", {"docs": docs}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def save_doc(request):
    if request.is_ajax():
        file_name = request.POST["file_name"]
        fname = file_name if file_name.split('.')[-1] == json else file_name + ".html"

        # Save to database and fs
        doc = Document()
        doc.teacher = request.user
        doc.doc_file.save(fname, ContentFile(request.POST["html_data"]))

    return ajax_resp("Action performed")


@login_required(login_url='/login/')
def load_doc(request, id_doc):
    doc = Document.objects.get(pk=id_doc)
    data = doc.doc_file.read()
    return ajax_resp(data)


@login_required(login_url='/login/')
def remove_doc(request, id_doc):
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


@login_required(login_url='/login/')
def papers(request):
    pps = Papers.objects.filter(teacher=request.user)
    return render_to_response("papers.html", {"papers": pps}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_paper(request):
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


@login_required(login_url='/login/')
def remove_paper(request, id_paper):
    p = Papers.objects.get(pk=id_paper)
    if p.paper_file:
        os.remove(p.paper_file.path)
    p.delete()

    return redirect("/papers/")