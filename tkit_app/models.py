from django.db import models
from django.contrib.auth.models import User


class Classes(models.Model):
    name = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User)


#def upload_to(instance, filename):
#    return '/static/img/%s/%s' % (instance.user.user.username, filename)


class Students(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    parent = models.CharField(max_length=100)
    parent_email = models.EmailField()
    photo = models.ImageField(upload_to="/static/img/", blank=True, null=True)
    s_class = models.ForeignKey(Classes)


class Attendance(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=50)
    student = models.ForeignKey(Students)


class Notes(models.Model):
    n_type = models.BooleanField()
    date = models.DateField(blank=True, null=True, auto_now_add=True)
    comment = models.TextField()
    student = models.ForeignKey(Students)


class Grades(models.Model):
    subject = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True, auto_now_add=True)
    grade = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=50)
    student = models.ForeignKey(Students)


class Lessons(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(blank=True, null=True, auto_now_add=True)
    teacher = models.ForeignKey(User)


class Assignments(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_begin = models.DateField(blank=True, null=True, auto_now_add=True)
    date_end = models.DateField()
    a_class = models.ForeignKey(Classes)


class Settings(models.Model):
    absence_limit = models.IntegerField()
    spc_limit = models.IntegerField()  # students per class
    negative_notes_limit = models.IntegerField()
    #color_scheme = models.CharField(max_length=50)
    teacher = models.ForeignKey(User)


class ToDoList(models.Model):
    title = models.CharField(max_length=60)
    date_exp = models.DateField()
    teacher = models.ForeignKey(User)