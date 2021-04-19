from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import StudentForm, UserRegisterForm


@login_required
def home(request):
    try:
        student = request.user.student
    except User.student.RelatedObjectDoesNotExist:
        return redirect("students:create")

    context = {"student": student}

    return render(request, "students/home.html", context)


@login_required
def create(request):
    instance = getattr(request.user, "student", None)

    if instance:
        messages.success(request, "Already created!")  # Needs a better message

        return redirect("students:home")

    if request.POST:
        form = StudentForm(request.POST)

        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user
            s.save()
            print(f"{s.transcript=}")
            messages.success(request, "Success")

            return redirect("students:home")
        else:
            print("ERROR in s_form")
    else:
        form = StudentForm()
    context = {"form": form}

    return render(request, "students/student.html", context=context)


def register(request):
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        messages.success(request, "Your account has been created!")
        form.save()

        return redirect("students:login")

    return render(request, "students/register.html", {"form": form})
