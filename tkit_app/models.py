from django.db import models
from django.contrib.auth.models import User
import os


def get_ord_path(instance, filename):
    return os.path.join(str(instance.teacher.username), filename)


def get_student_path(instance, filename):
    return os.path.join(str(instance.s_class.teacher.username), filename)


def get_board_path(instance, filename):
    return os.path.join(str(instance.lesson.teacher.username), filename)


class Classes(models.Model):
    name = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User)


class Students(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    parent = models.CharField(max_length=100)
    parent_email = models.EmailField()
    photo = models.ImageField(upload_to=get_student_path, blank=True, null=True)
    s_class = models.ForeignKey(Classes)


class Attendance(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=50)
    student = models.ForeignKey(Students)


class Notes(models.Model):
    n_type = models.BooleanField()
    date = models.DateField()
    comment = models.TextField()
    student = models.ForeignKey(Students)


class Grades(models.Model):
    subject = models.CharField(max_length=50)
    date = models.DateField()
    grade = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=50)
    student = models.ForeignKey(Students)


class Lessons(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    teacher = models.ForeignKey(User)


class Boards(models.Model):
    b_file = models.ImageField(upload_to=get_board_path)
    lesson = models.ForeignKey(Lessons)


class Assignments(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_begin = models.DateField()
    date_end = models.DateField()
    a_class = models.ForeignKey(Classes)


class Settings(models.Model):
    absence_limit = models.IntegerField(null=True, blank=True, default=60)
    spc_limit = models.IntegerField(null=True, blank=True, default=30)  # students per class
    negative_notes_limit = models.IntegerField(null=True, blank=True, default=30)
    color_scheme = models.CharField(max_length=50, null=True, blank=True, default="skin-blue")
    teacher = models.ForeignKey(User)


class ToDoList(models.Model):
    title = models.CharField(max_length=60)
    date_exp = models.DateField()
    percentage = models.IntegerField()
    teacher = models.ForeignKey(User)


class MindMap(models.Model):
    json_file = models.FileField(upload_to=get_ord_path)
    teacher = models.ForeignKey(User)


class Presentation(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    pres_file = models.FileField(upload_to=get_ord_path)
    teacher = models.ForeignKey(User)


class Document(models.Model):
    doc_file = models.FileField(upload_to=get_ord_path)
    teacher = models.ForeignKey(User)


class Papers(models.Model):
    paper_file = models.FileField(upload_to=get_ord_path)
    title = models.CharField(max_length=150)
    abstract = models.TextField()
    teacher = models.ForeignKey(User)