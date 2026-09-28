from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.contrib.auth.models import Group
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        from main.models import Interest, Project, Experience

        editor_group, _ = Group.objects.get_or_create(name="Editor")

        content_types = {
            "experience": ContentType.objects.get_for_model(Experience),
            "interest": ContentType.objects.get_for_model(Interest),
            "project": ContentType.objects.get_for_model(Project),
        }

        change_permissions = Permission.objects.filter(
            content_type__in=content_types.values(),
            codename__in=["change_experience", "change_interest", "change_project"],
        )

        editor_group.permissions.set(change_permissions)
