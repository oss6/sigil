from django.shortcuts import render
from models import *


def classes(request):
    return render(request, "classes.html")


def students(request, class_name):
    pass


def my_lessons(request):
    pass