from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
from main.models import Experience
from main.models import Interest, Project
from main.forms import InterestForm, ProjectForm

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
import datetime 
from django.contrib.auth.decorators import login_required  # Tambahkan baris ini
from django.core.exceptions import PermissionDenied        # Tambahkan baris ini

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST


def user_is_editor(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name="Editor").exists()
    )


def can_update_model(user, model_name):
    return user.is_superuser or user.has_perm(f"main.change_{model_name}")


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Maulana Farrel Arvindra",
        "npm": "2506552802",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Farrel",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Burhan",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)
    
@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Farrel",
        "form": form,
        "is_edit": False,
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not can_update_model(request.user, "project"):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {"name": "Farrel", "form": form, "is_edit": True, "project": project}
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


def show_interest(request):
    context = {
        "name": "Farrel",
        "interest_list": Interest.objects.all(),
    }

    return render(request, "interest.html", context)


@require_GET
def get_interests_json(request):
    title_query = request.GET.get("title", "").strip()
    interests = Interest.objects.prefetch_related("interested_users").all()

    if title_query:
        interests = interests.filter(title__icontains=title_query)

    data = []
    for interest in interests:
        interested_users = interest.interested_users.all()
        is_interested = (
            request.user in interested_users if request.user.is_authenticated else False
        )
        data.append(
            {
                "pk": str(interest.id),
                "fields": {
                    "title": interest.title,
                    "description": interest.description,
                    "since": interest.since,
                    "star_count": interested_users.count(),
                    "is_starred": is_interested,
                },
            }
        )

    return JsonResponse(data, safe=False)


@require_POST
def create_interest_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan interest."},
            status=403,
        )

    form = InterestForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    interest = form.save()
    return JsonResponse(
        {
            "message": "Interest berhasil ditambahkan.",
            "pk": str(interest.id),
            "fields": {
                "title": interest.title,
                "description": interest.description,
                "since": interest.since,
                "star_count": 0,
                "is_starred": False,
            },
        },
        status=201,
    )


@login_required(login_url="/login/")
def create_interest(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = InterestForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Interest baru berhasil ditambahkan!")
        return redirect("main:show_interest")

    context = {
        "name": "Farrel",
        "form": form,
        "is_edit": False,
    }
    return render(request, "interests_form.html", context)


@login_required(login_url="/login/")
def update_interest(request, interest_id):
    if not can_update_model(request.user, "interest"):
        raise PermissionDenied

    interest = get_object_or_404(Interest, pk=interest_id)
    form = InterestForm(request.POST or None, instance=interest)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Interest berhasil diperbarui!")
        return redirect("main:show_interest")

    context = {"name": "Farrel", "form": form, "is_edit": True, "interest": interest}
    return render(request, "interests_form.html", context)


@login_required(login_url="/login/")
def delete_interest(request, interest_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    interest = get_object_or_404(Interest, pk=interest_id)

    if request.method == "POST":
        interest.delete()
        messages.success(request, "Interest berhasil dihapus!")

    return redirect("main:show_interest")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Farrel",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Farrel",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


@login_required(login_url="/login/")
def toggle_interest_star(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)

    if request.method == "POST":
        if request.user in interest.interested_users.all():
            interest.interested_users.remove(request.user)
        else:
            interest.interested_users.add(request.user)

    return redirect("main:show_interest")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)