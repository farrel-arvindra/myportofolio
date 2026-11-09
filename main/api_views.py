from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Interest, Project
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly,
    IsPortfolioOwnerOrReadOnly,
)
from main.serializers import InterestSerializer, ProjectSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    """
    List all projects (filtered optionally by ?title=) or create a new project.
    Only superuser may create.
    """
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    """
    Retrieve, update (PUT/PATCH), or delete a specific project by UUID.
    Only superuser may update or delete.
    """
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    """
    Toggle star status for the authenticated user on a project.
    """
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def interest_list(request):
    """
    List all interests (filtered optionally by ?title=) or create a new interest.
    Creation (POST) is restricted to portfolio owner (superuser).
    """
    if request.method in ("GET", "HEAD"):
        interests = Interest.objects.prefetch_related("interested_users").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            interests = interests.filter(title__icontains=title)
        serializer = InterestSerializer(
            interests, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = InterestSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def interest_detail(request, interest_id):
    """
    Retrieve, update (PUT/PATCH), or delete an interest by UUID.
    - Safe methods (GET, HEAD): all visitors.
    - PUT / PATCH: Editors and Superuser.
    - DELETE: Superuser only.
    """
    interest = get_object_or_404(
        Interest.objects.prefetch_related("interested_users"), pk=interest_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = InterestSerializer(interest, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = InterestSerializer(
        interest, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def interest_star(request, interest_id):
    """
    Toggle star status for the authenticated user on an interest.
    """
    interest = get_object_or_404(Interest, pk=interest_id)
    if interest.interested_users.filter(pk=request.user.pk).exists():
        interest.interested_users.remove(request.user)
    else:
        interest.interested_users.add(request.user)
    serializer = InterestSerializer(interest, context={"request": request})
    return Response(serializer.data)
