from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from forms import RegistrationForm
from models import *


def add_teacher(username, first_name, last_name, email):
    t = Teachers(username=username, first_name=first_name, last_name=last_name, email=email)
    t.save()


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            u = form.save()
            add_teacher(u.username, u.first_name, u.last_name, u.email)
            return redirect('/signup-success/')
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()

    return render(request, 'registration/register.html', args)


@login_required(login_url='/login/')
def classes(request):
    cls = []

    if request.user.is_authenticated():
        cls = Classes.objects.all().filter(teacher=request.user.username)

    return render_to_response("classes.html", {"classes": cls})


@login_required(login_url='/login/')
def add_class(request):
    cl_name = request.cleaned_data['class_name']
    school = request.cleaned_data['school']
    desc = request.cleaned_data['desc']

    cl = Classes(name=cl_name, school=school, description=desc, teacher=request.user.username)
    cl.save()

    return render_to_response("classes.html")


@login_required(login_url='/login/')
def students(request, class_name):
    pass


@login_required(login_url='/login/')
def my_lessons(request):
    pass