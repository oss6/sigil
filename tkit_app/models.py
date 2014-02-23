from django.db import models
from django.contrib.auth.models import User


class Classes(models.Model):
    name = models.CharField(max_length=20)
    school = models.CharField(max_length=20)
    description = models.TextField()
    teacher = models.ForeignKey(User)


#def upload_to(instance, filename):
#    return '/static/img/%s/%s' % (instance.user.user.username, filename)


class Students(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    parent = models.CharField(max_length=30)
    parent_email = models.EmailField()
    photo = models.ImageField(upload_to="/static/img/", blank=True, null=True)
    s_class = models.ForeignKey(Classes)


class Attendance(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=30)
    student = models.ForeignKey(Students)


class Notes(models.Model):
    date = models.DateField()
    comment = models.TextField()
    student = models.ForeignKey(Students)


class Grades(models.Model):
    subject = models.CharField(max_length=20)
    grade = models.IntegerField()
    type = models.CharField(max_length=20)
    student = models.ForeignKey(Students)


class Lessons(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    teacher = models.ForeignKey(User)