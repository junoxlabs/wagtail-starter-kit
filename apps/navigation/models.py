from django.db import models
from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class MenuItem(Orderable):
    """
    Menu item snippet that can be used to create navigation menus with nested support.
    """

    link_title = models.CharField(
        max_length=50, blank=True, help_text="Title to display for this menu item"
    )

    link_url = models.CharField(
        max_length=500, blank=True, help_text="URL for this menu item"
    )

    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
        help_text="Page for this menu item",
    )

    open_in_new_tab = models.BooleanField(
        default=False, help_text="Open this link in a new tab"
    )

    # Add parent relationship for nested menus
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
        help_text="Parent menu item for nested menus",
    )

    # Define the parent menu (either top-level menu or parent item)
    menu = ParentalKey("Menu", related_name="menu_items", on_delete=models.CASCADE)

    sort_order = models.PositiveIntegerField(default=0, editable=False)

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("open_in_new_tab"),
        FieldPanel("parent"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return "#"

    @property
    def title(self):
        if self.link_title:
            return self.link_title
        elif self.link_page:
            return self.link_page.title
        return "Missing Title"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"


class Menu(ClusterableModel):
    """
    Menu snippet that contains hierarchical menu items.
    """

    title = models.CharField(max_length=100, help_text="Title for this menu")

    slug = models.SlugField(
        unique=True, max_length=100, help_text="Unique slug for this menu"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Items", heading="Top Level Menu Items"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"

    def get_root_menu_items(self):
        """Get top-level menu items (those without a parent)"""
        return self.menu_items.filter(parent=None).order_by("sort_order")

    def get_menu_tree(self):
        """Get the complete menu tree with nested structure"""
        root_items = self.get_root_menu_items()
        tree = []

        for item in root_items:
            tree.append({"item": item, "children": self._get_children(item)})

        return tree

    def _get_children(self, parent_item):
        """Recursively get children for a menu item"""
        children = parent_item.children.all().order_by("sort_order")
        result = []

        for child in children:
            result.append({"item": child, "children": self._get_children(child)})

        return result
