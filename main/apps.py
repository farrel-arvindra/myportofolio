import sys
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_editor_group(sender, **kwargs):
    if "test" in sys.argv:
        return
    try:
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        from main.models import Experience, Interest, Project

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
    except Exception:
        pass


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self):
        post_migrate.connect(create_editor_group, sender=self)
