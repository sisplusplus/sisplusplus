from django.db import models

from sis.models import Course


class CourseT(models.Model):
    LetterGrade = models.TextChoices("LetterGrade",
                                     "AA BA BB CB CC DC DD FF VF")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(
        max_length=2, choices=LetterGrade.choices, default=LetterGrade.AA
    )
    failed_before = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.code} - {self.grade}"


class Term(models.Model):
    name = models.CharField(max_length=20)
    courses = models.ManyToManyField(CourseT)

    def __str__(self):
        return self.name


class Transcript(models.Model):
    terms = models.ManyToManyField(Term)
