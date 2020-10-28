from django.contrib import admin
from .models import Faculty, Program, Curriculum, Course, Semester


# Register your models here.
class FacultyAdmin(admin.ModelAdmin):
    fields = ['name']


class ProgramAdmin(admin.ModelAdmin):
    fields = ['name', 'faculty']


class CurriculumAdmin(admin.ModelAdmin):
    fields = ['program', 'to_year', 'from_year']


class CourseAdmin(admin.ModelAdmin):
    fields = ['code', 'title', 'credit']


class SemesterAdmin(admin.ModelAdmin):
    fields = ['curriculum', 'num', 'courses']


admin.site.register(Faculty)
admin.site.register(Program)
admin.site.register(Curriculum)
admin.site.register(Course)
admin.site.register(Semester)

# admin.site.register(Faculty, FacultyAdmin)
# admin.site.register(Program, ProgramAdmin)
# admin.site.register(Curriculum, CurriculumAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Semester, SemesterAdmin)
