from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
from main.models import Experience
from main.models import Interest
from main.forms import InterestForm


def show_main(request):
    context = {
        "name": "Maulana Farrel Arvindra",
        "npm": "2506552802",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Maulana Farrel Arvindra",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_interest(request):
    context = {
        "name": "Maulana Farrel Arvindra",
        "interest_list": Interest.objects.all(),
    }

    return render(request, "interest.html", context)

def create_interest(request):
    form = InterestForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Interest baru berhasil ditambahkan!")
        return redirect("main:show_interest")

    context = {
        "name": "Maulana Farrel Arvindra",
        "form": form,
    }
    return render(request, "interests_form.html", context)