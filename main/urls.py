from django.urls import path

from main.views import show_main, show_experience, show_interest, create_interest, register, login_user, logout_user, toggle_star, show_projects, get_projects_json

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("interest/", show_interest, name='show_interest'),
    path("interest/add/", create_interest, name="create_interest"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("projects/", show_projects, name="show_projects"),
    # Tambahkan path ini ke dalam urlpatterns
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
    path("api/projects/", get_projects_json, name="get_projects_json")
]