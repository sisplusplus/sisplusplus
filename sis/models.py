from django.db import models

# Create your models here.

# When altering models in this file make sure to reflect it on crawler on sis/crawler

FACULTY_CHOICES_TURKISH = [("IN", "İnşaat Fakültesi"),
                           ("MM", "Mimarlık Fakültesi"),
                           ("MK", "Makina Fakültesi"),
                           ("EE", "Elektrik - Elektronik Fakültesi"),
                           ("MD", "Maden Fakültesi"),
                           ("KM", "Kimya - Metalurji Fakültesi"),
                           ("IS", "İşletme Fakültesi"),
                           ("GD", "Gemi İnşaatı ve Deniz Bilimleri Fakültesi"),
                           ("FE", "Fen - Edebiyat Fakültesi"),
                           ("UU", "Uçak ve Uzay Bilimleri Fakültesi"),
                           ("KO", "Türk Musikisi Devlet Konservatuarı"),
                           ("DZ", "Denizcilik Fakültesi"),
                           ("TK",
                            "Tekstil Teknolojileri ve Tasarımı Fakültesi"),
                           ("BB", "Bilgisayar ve Bilişim Fakültesi"),
                           ("SN", "Uluslararası Ortak Lisans Programları"),
                           ("KK", "İTÜ Kuzey Kıbrıs")]

FACULTY_CHOICES = [("IN", "Faculty of Civil Engineering"),
                   ("MM", "Faculty of Architecture"),
                   ("MK", "Faculty of Mechanical Engineering"),
                   ("EE", "Faculty of Electrical and Electronic Engineering"),
                   ("MD", "Faculty of Mines"),
                   ("KM", "Faculty of Chemical and Metallurgical Engineering"),
                   ("IS", "Faculty of Management"),
                   ("GD",
                    "Faculty of Naval Architecture and Ocean Engineering"),
                   ("FE", "Faculty of Science and Letters"),
                   ("UU", "Faculty of Aeronautics and Astronautics"),
                   ("KO", "Turkish Music State Conservatory"),
                   ("DZ", "Maritime Faculty"),
                   ("TK", "Faculty of Textile Technologies and Design"),
                   ("BB", "Faculty of Computer and Informatics Engineering"),
                   ("SN", "Dual Degree Undergraduate Programs"),
                   ("KK", "ITU North Cyprus")]


class Faculty(models.Model):
    code = models.CharField(primary_key=True, max_length=2,
                            choices=FACULTY_CHOICES)
    fullName = models.CharField(max_length=255, default="")

    def __str__(self):
        return ' - '.join((self.code, self.fullName))


class Program(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    fullName = models.CharField(max_length=200, default="")
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


