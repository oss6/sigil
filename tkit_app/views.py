from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
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

    return render(request, 'register.html', args)


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect("/account/loggedin/")
    else:
        return redirect("/account/invalid/")


def logout(request):
    pass


def classes(request):
    return render_to_response("classes.html")


def students(request, class_name):
    pass


def my_lessons(request):
    pass