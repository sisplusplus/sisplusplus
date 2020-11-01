from django.contrib import admin
from .models import (
    Faculty,
    Program,
    Curriculum,
    Course,
    Semester,
    SemesterCourseSlot,
)


# Register your models here.


def semester_courses(semester):
    if semester.code:
        toReturn = ""
        for semestercourseslot in semester.semestercourseslot_set.all():
            for num, course in enumerate(semestercourseslot.courses.all()):
                toReturn += f"{course.code}" if num < 1 else f" or {course.code}"
            toReturn += ", "
        return toReturn
    else:
        return "-"


class ProgramInline(admin.TabularInline):
    model = Program
    extra = 0


class CurriculumInline(admin.TabularInline):
    model = Curriculum
    extra = 0


class SemesterInline(admin.TabularInline):
    model = Semester
    fields = [semester_courses]
    readonly_fields = [semester_courses]
    extra = 0


class SemesterCourseSlotInline(admin.TabularInline):
    model = SemesterCourseSlot
    autocomplete_fields = ["courses"]


# class CourseInline(admin.StackedInline):
# model = Course
# extra = 3


class FacultyAdmin(admin.ModelAdmin):
    inlines = [ProgramInline]


class ProgramAdmin(admin.ModelAdmin):
    inlines = [CurriculumInline]


class CurriculumAdmin(admin.ModelAdmin):
    inlines = [SemesterInline]


class SemesterAdmin(admin.ModelAdmin):
    inlines = [SemesterCourseSlotInline]


class SemesterCourseSlotAdmin(admin.ModelAdmin):
    autocomplete_fields = ["courses"]


class CourseAdmin(admin.ModelAdmin):
    ordering = ["code"]
    search_fields = ["code"]


# admin.site.register(Faculty)
# admin.site.register(Program)
# admin.site.register(Curriculum)
# admin.site.register(Course)
# admin.site.register(Semester)
# admin.site.register(SemesterCourseSlot)

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(SemesterCourseSlot, SemesterCourseSlotAdmin)
