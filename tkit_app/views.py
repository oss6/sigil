from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
# from django.contrib import auth
from forms import RegistrationForm, AddClassForm
from django.template import RequestContext
from models import *


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
    return render_to_response("classes.html", {"classes": cls})


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
def remove_class(request, class_name):
    c = Classes.objects.get(name=class_name)
    c.delete()

    return redirect('/classes/')


@login_required(login_url='/login/')
def students(request, class_name):
    cl = Classes.objects.all().filter(name__exact=class_name, teacher__exact=request.user)[0]
    ss = Students().objects.all().filter(s_class=cl)




@login_required(login_url='/login/')
def lessons(request):
    pass