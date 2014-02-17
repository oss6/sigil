from django.db import models


class Classes(models.Model):
    name = models.CharField(max_length=20)
    school = models.CharField(max_length=20)


class Students(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    parent = models.CharField(max_length=30)
    parent_email = models.EmailField()
    photo = models.ImageField(upload_to='/', blank=True, null=True)


class Attendance(models.Model):
    pass


class Notes(models.Model):
    pass


class Grades(models.Model):
    pass