from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import StudentRegisterForm


@login_required
def home(request):
    return render(request, 'students/home.html')


def register(request):
    form = StudentRegisterForm(request.POST or None)

    if form.is_valid():
        messages.success(request, "Your account has been created!")
        form.save()

        return redirect("students:login")

    return render(request, "students/register.html", {"form": form})
