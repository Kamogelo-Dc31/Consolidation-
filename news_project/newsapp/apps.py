# newsapp/apps.py

from django.apps import AppConfig
import logging


class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'

    def ready(self):
        import newsapp.signals  # Safe to import here

        # Avoid DB queries during migration/initialization
        try:
            from django.db.utils import OperationalError, ProgrammingError
            from django.contrib.auth.models import Group

            roles = ['Reader', 'Editor', 'Journalist']
            for role in roles:
                Group.objects.get_or_create(name=role)

        except (OperationalError, ProgrammingError) as e:
            # Avoid crashing on migrate/makemigrations
            logging.warning(f"Skipped role creation during app initialization: {e}")
