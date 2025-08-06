from django.apps import AppConfig


class NavigationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.navigation"
    verbose_name = "Navigation"
    
    def ready(self):
        # Import template tags to ensure they're registered
        from .templatetags import navigation_tags  # noqa
