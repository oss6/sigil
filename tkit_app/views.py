from django.shortcuts import render


def classes(request):
    return render(request, "classes.html")


def students(request, class_name):
    pass