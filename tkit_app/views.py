from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from forms import RegistrationForm
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
def classes(request):
    cls = []

    return render_to_response("classes.html")


@login_required(login_url='/login/')
def students(request, class_name):
    pass


@login_required(login_url='/login/')
def my_lessons(request):
    pass