from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    path("interests/", api_views.interest_list, name="interest-list"),
    path("interests/<uuid:interest_id>/", api_views.interest_detail, name="interest-detail"),
    path("interests/<uuid:interest_id>/star/", api_views.interest_star, name="interest-star"),
]
