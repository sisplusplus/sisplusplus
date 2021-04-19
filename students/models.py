from django.db import models
from django.contrib.auth.models import User

from smart_selects.db_fields import ChainedForeignKey

from sis.models import Curriculum, Faculty, Program
from transcript.models import Transcript


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=9)
    name = models.CharField(max_length=100, default="")
    surname = models.CharField(max_length=100, default="")

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    program = ChainedForeignKey(
        Program, chained_field="faculty", chained_model_field="faculty"
    )
    curriculum = ChainedForeignKey(
        Curriculum, chained_field="program", chained_model_field="program"
    )

    transcript = models.OneToOneField(Transcript, on_delete=models.CASCADE,
                                      null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
