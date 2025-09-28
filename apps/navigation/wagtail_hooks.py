from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel
from django.utils.translation import gettext_lazy as _
from .models import Menu


class MenuAdmin(SnippetViewSet):
    model = Menu
    
    # Add search fields for better admin experience
    search_fields = ["title", "slug"]
    
    # Add list display for better overview
    list_display = ["title", "slug"]
    
    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", heading="Menu Items", label="Menu Item"),
    ]
    
    @property
    def icon(self):
        return "bars"
    
    @property
    def menu_label(self):
        return "Navigation Menus"
    
    @property
    def menu_name(self):
        return "navigation_menus"
    
    @property
    def menu_order(self):
        return 100


# Register the Menu model as a snippet with the custom admin interface
register_snippet(MenuAdmin)


# Add a hook to add the navigation menu to the main admin menu
@hooks.register("register_admin_menu_item")
def register_navigation_menu():
    # Use the correct URL pattern for Wagtail snippets
    return MenuItem(
        _("Navigation"),
        "/admin/snippets/navigation/menu/",
        icon_name="bars",
        order=100,
    )
