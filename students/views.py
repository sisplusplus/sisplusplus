from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import StudentRegisterForm


def register(request):
    form = StudentRegisterForm(request.POST or None)

    if form.is_valid():
        messages.success(request, "Your account has been created!")
        form.save()

        return redirect("login")

    return render(request, "students/register.html", {"form": form})
