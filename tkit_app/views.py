from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Min, Max
from forms import *
from models import *
from datetime import timedelta
import json
import datetime


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
            return redirect('/signup-success/')
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()

    return render(request, 'registration/register.html', args)


@login_required(login_url='/login/')
def disable_account(request):
    u = request.user
    u.is_active = False


@login_required(login_url='/login/')
def classes(request):
    cls = Classes.objects.all().filter(teacher=request.user)
    return render_to_response("classes.html", {"classes": cls}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_class(request):
    if request.method == "POST":
        form = AddClassForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            cl_name = form.cleaned_data["name"]
            school = form.cleaned_data["school"]
            desc = form.cleaned_data["description"]

            # Save class into db
            cl = Classes(name=cl_name, school=school, description=desc, teacher=request.user)
            cl.save()

            return redirect('/classes/')
    else:
        form = AddClassForm()

    return render_to_response('add-class.html', {"form": form}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def remove_class(request, id_class):
    if request.is_ajax():
        c = Classes.objects.get(pk=id_class)
        c.delete()

    return ajax_resp("Class removed")


# TODO: CLASS REPORT!
@login_required(login_url='/login/')
def class_report(request, id_class):
    pass


@login_required(login_url='/login/')
def students(request, id_class):
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.all().filter(s_class=cl)

    return render_to_response("students.html", {"students": ss, "class": cl, "nums": len(ss)},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_student(request, id_class):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            parent = form.cleaned_data["parent"]
            parent_email = form.cleaned_data["parent_email"]
            photo = form.cleaned_data["photo"]

            # Save student into db
            c = Classes.objects.get(pk=id_class)
            s = Students(first_name=first_name, last_name=last_name,
                         email=email, parent=parent, parent_email=parent_email, photo=photo, s_class=c)
            s.save()

            return redirect('/classes/' + id_class + '/students/')
    else:
        form = AddStudentForm()

    return render_to_response('add-student.html', {"form": form}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def remove_student(request, id_class, id_student):
    if request.is_ajax():
        s = Students.objects.get(pk=id_student)
        s.delete()

    return ajax_resp("Student removed")


@login_required(login_url='/login/')
def student_info(request, id_student):
    student = Students.objects.get(pk=id_student)
    return render_to_response("student-report.html", {"student": student}, context_instance=RequestContext(request))


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


"""def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)"""


@login_required(login_url='/login/')
def grades_performance_chart(request, id_student):
    student = Students.objects.get(pk=id_student)
    #grades = Grades.objects.filter(student=student)
    oldest_date = Grades.objects.aggregate(Min('date'))['date__min']
    newest_date = Grades.objects.aggregate(Max('date'))['date__max']
    grades_ranges = []
    grades_range = Grades.objects.filter(date__range=["2011-01-01", "2011-01-31"])

    rows = [{"c": [{"v": g.subject, "f": None}, {"v": g.grade, "f": None}]} for g in grades_range]

    j = json.dumps({
        "cols": [
            {"id": "", "label": "Subject", "pattern": "", "type": "string"},
            {"id": "", "label": "Grade", "pattern": "", "type": "number"}
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
    else:
        form = AddNoteForm()

    return render_to_response('add-note.html', {"form": form}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def grade_book(request, id_class):
    cl = Classes.objects.get(pk=id_class)
    ss = Students.objects.all().filter(s_class=cl)
    grades = Grades.objects.all().filter(student__in=[student for student in ss])

    return render_to_response("grade-book.html", {"students": ss, "class": cl, "grades": grades},
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
    else:
        form = AddGradableItemForm()

    return render_to_response('add-gradable.html', {"form": form}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def update_grade(request, id_grade, grade):
    if request.is_ajax():
        g = Grades.objects.get(pk=id_grade)
        g.grade = grade
        g.save()

    return ajax_resp("Grade updated")


@login_required(login_url='/login/')
def attendance(request, class_name):
    pass


@login_required(login_url='/login/')
def lessons(request):
    cls = Lessons.objects.all().filter(teacher=request.user)
    return render_to_response("lessons.html", {"lessons": cls}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_lesson(request):
    if request.method == "POST":
        form = AddLessonForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            date = form.cleaned_data["date"]

            # Save lesson into db
            l = Lessons(title=title, description=desc, date=date, teacher=request.user)
            l.save()

            return redirect('/lessons/')
    else:
        form = AddLessonForm()

    return render_to_response('add-lesson.html', {"form": form}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def remove_lesson(request, id_lesson):
    if request.is_ajax():
        l = Lessons.objects.get(pk=id_lesson)
        l.delete()

    return ajax_resp("Lesson removed")


@login_required(login_url='/login/')
def homework(request, id_class):
    cl = Classes.objects.get(pk=id_class)
    assm = Assignments.objects.all().filter(a_class=cl)
    return render_to_response("assignments.html", {"assignments": assm, "class": cl}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_assignment(request, id_class):
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
            assm = Assignments(title=title, description=desc, date_begin=begin, date_end=end, a_class=cl)
            assm.save()

            return redirect('/classes/' + str(id_class) + '/homework/')
    else:
        form = AddAssignmentForm()

    return render_to_response('add-assignment.html', {"form": form}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def remove_assignment(request, id_class, id_assignment):
    if request.is_ajax():
        cl = Classes.objects.get(pk=id_class)
        assm = Assignments.objects.get(pk=id_assignment, a_class=cl)
        assm.delete()

    return ajax_resp("Assignment removed")