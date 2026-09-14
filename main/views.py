from django.shortcuts import render

# Create your views here.
from main.models import Experience
from main.models import Interest 


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