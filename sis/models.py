from django.db import models

# Create your models here.

# When altering models in this file make sure to reflect it on crawler on sis/crawler


class Faculty(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return " - ".join((self.code, self.full_name))


class Program(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    full_name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.faculty.code + " faculty's " + self.code + " program."

    def __repr__(self):
        return self.code + " Program"


class Curriculum(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    url = models.URLField()
    code = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.program.full_name + ": " + self.full_name


class Course(models.Model):
    code = models.CharField(max_length=8, primary_key=True)
    title = models.CharField(max_length=100)
    credit = models.FloatField(null=True)
    theoretical = models.PositiveSmallIntegerField(null=True, blank=True)
    tutorial = models.PositiveSmallIntegerField(null=True, blank=True)
    lab = models.PositiveSmallIntegerField(null=True, blank=True)
    is_compulsary = models.BooleanField()
    ects = models.FloatField(default=0, null=True)
    prerequisites = models.CharField(max_length=1000)
    class_restrictions = models.CharField(max_length=20)

    def __str__(self):
        return self.code


class Semester(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    num = models.PositiveSmallIntegerField()
    code = models.CharField(max_length=30, primary_key=True)
    # total_ects = models.FloatField()
    # total_credits = models.FloatField()

    def __str__(self):
        return self.code


class SemesterCourseSlot(models.Model):
    # This is meant to be a transitional model
    code = models.CharField(max_length=35, primary_key=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.code + " " + self.title
