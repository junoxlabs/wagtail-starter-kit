from django.apps import AppConfig
from django.db import transaction
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class NavigationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.navigation"

    def ready(self):
        super().ready()
        
        # Import signal handlers
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate)
        def create_default_menus_handler(sender, **kwargs):
            if sender.name == self.name:
                self.create_default_menus()

    def create_default_menus(self):
        """Create default menus after the app is loaded."""
        try:
            from .models import Menu
            
            # Use transaction to ensure atomicity
            with transaction.atomic():
                # Create main menu if it doesn't exist
                Menu.objects.get_or_create(
                    slug="main-menu", defaults={"title": "Navbar Menu"}
                )

                # Create footer menu if it doesn't exist
                Menu.objects.get_or_create(
                    slug="footer-menu", defaults={"title": "Footer Menu"}
                )

                # Create legal menu if it doesn't exist
                Menu.objects.get_or_create(
                    slug="legal-menu", defaults={"title": "Legal Menu"}
                )
                
                # Clear cache for menus since we've created new ones
                cache.delete_many(["menu_tree_main-menu", "menu_tree_footer-menu", "menu_tree_legal-menu"])
                
        except Exception as e:
            # If there's an issue with the database (e.g., not migrated yet),
            # we skip creating the default menus. They will be created later.
            logger.warning(f"Could not create default menus: {str(e)}")
            pass
