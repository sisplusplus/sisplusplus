from django.contrib import admin
from .models import Faculty, Program, Curriculum, Course, Semester


# Register your models here.
class ProgramInline(admin.StackedInline):
    model = Program
    extra = 3

class CurriculumInline(admin.StackedInline):
    model = Curriculum
    extra = 3

class SemesterInline(admin.StackedInline):
    model = Semester
    extra = 3

# class CourseInline(admin.StackedInline):
    # model = Course
    # extra = 3
    
class FacultyAdmin(admin.ModelAdmin):
    inlines=[ProgramInline]

class ProgramAdmin(admin.ModelAdmin):
    inlines=[CurriculumInline]


class CurriculumAdmin(admin.ModelAdmin):
    inlines=[SemesterInline]

# class SemesterAdmin(admin.ModelAdmin):
    # inlines=[CourseInline]


# admin.site.register(Faculty)
# admin.site.register(Program)
# admin.site.register(Curriculum)
admin.site.register(Course)
admin.site.register(Semester)

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Semester, SemesterAdmin)
