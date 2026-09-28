from django.urls import path

from main.views import show_main, show_experience, show_interest, create_interest, register, login_user, logout_user, toggle_star, show_projects, get_projects_json
import main.views as views
app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),

    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", views.create_project, name="create_project"),
    path("projects/<uuid:project_id>/edit/", views.update_project, name="update_project"),
    path("projects/<uuid:project_id>/delete/", views.delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),

    path("interest/", show_interest, name='show_interest'),
    path("interest/add/", create_interest, name="create_interest"),
    path("interest/<uuid:interest_id>/edit/", views.update_interest, name="update_interest"),
    path("interest/<uuid:interest_id>/delete/", views.delete_interest, name="delete_interest"),
    path("interest/<uuid:interest_id>/star/", views.toggle_interest_star, name="toggle_interest_star"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]