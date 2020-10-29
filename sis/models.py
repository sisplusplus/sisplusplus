from django.db import models

# Create your models here.

# When altering models in this file make sure to reflect it on crawler on sis/crawler

class Faculty(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    full_name = models.CharField(max_length=255, default="")

    def __str__(self):
        return ' - '.join((self.code, self.full_name))


class Program(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    full_name = models.CharField(max_length=200, default="")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.faculty.code + " faculty's " + self.code + ' program.'

    def __repr__(self):
        return self.code + ' Program'


class Curriculum(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    from_year = models.PositiveSmallIntegerField(null=True, blank=True)
    to_year = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.program.name + " program's curriculum for years between"


class Course(models.Model):
    code = models.CharField(max_length=8, primary_key=True)
    title = models.CharField(max_length=100)
    credit = models.FloatField(null=True)
    theoretical = models.PositiveSmallIntegerField(null=True, blank=True)
    tutorial = models.PositiveSmallIntegerField(null=True, blank=True)
    lab = models.PositiveSmallIntegerField(null=True, blank=True)
    ects = models.FloatField(default=0, null=True)
    
    def __str__(self):
        return self.code

class Semester(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    num = models.PositiveSmallIntegerField()
    courses = models.ManyToManyField(Course)
    total_ects = models.FloatField()
    total_credits = models.FloatField()

    def __str__(self):
        return f"{self.num}. Semester - Total Credits: {self.total_credits} - " \
               f"Total ECTS: {self.total_ects}"


