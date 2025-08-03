from django.db import models
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


@register_snippet
class MenuItem(Orderable):
    """
    Menu item snippet that can be used to create navigation menus.
    """
    link_title = models.CharField(
        max_length=50,
        blank=True,
        help_text="Title to display for this menu item"
    )
    
    link_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="URL for this menu item"
    )
    
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
        help_text="Page for this menu item"
    )
    
    open_in_new_tab = models.BooleanField(
        default=False,
        help_text="Open this link in a new tab"
    )
    
    page = ParentalKey(
        'Menu',
        related_name='menu_items',
        on_delete=models.CASCADE
    )
    
    panels = [
        FieldPanel('link_title'),
        FieldPanel('link_url'),
        FieldPanel('link_page'),
        FieldPanel('open_in_new_tab'),
    ]
    
    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'
        
    @property
    def title(self):
        if self.link_title:
            return self.link_title
        elif self.link_page:
            return self.link_page.title
        return 'Missing Title'
        
    def __str__(self):
        return self.title


@register_snippet
class Menu(ClusterableModel):
    """
    Menu snippet that contains menu items.
    """
    title = models.CharField(
        max_length=100,
        help_text="Title for this menu"
    )
    
    slug = models.SlugField(
        max_length=100,
        help_text="Unique slug for this menu"
    )
    
    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        InlinePanel('menu_items', label="Menu Items")
    ]
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"
