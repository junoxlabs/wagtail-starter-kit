from django.db import models
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock

from apps.core.models import BasePage


class HomePage(BasePage):
    """
    HomePage model that inherits from BasePage.
    This is the main entry point for the website.
    """
    
    # Main content area as a StreamField for flexible content
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        # Add more blocks as needed for the homepage
    ], use_json_field=True, blank=True)
    
    # Additional fields specific to the homepage
    banner_title = models.CharField(max_length=255, blank=True, null=True)
    banner_subtitle = models.CharField(max_length=255, blank=True, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    content_panels = BasePage.content_panels + [
        FieldPanel('banner_title'),
        FieldPanel('banner_subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('body'),
    ]
    
    promote_panels = BasePage.promote_panels
    settings_panels = BasePage.settings_panels
    
    # Allow only one homepage to be created
    max_count = 1
    
    # Specify the template for this page
    template = "pages/home_page.html"
    
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


class StandardPage(BasePage):
    """
    StandardPage model that inherits from BasePage.
    Used for regular content pages with flexible body content.
    """
    
    # Main content area as a StreamField for flexible content
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = BasePage.content_panels + [
        FieldPanel('body'),
    ]
    
    promote_panels = BasePage.promote_panels
    settings_panels = BasePage.settings_panels
    
    # Specify the template for this page
    template = "pages/standard_page.html"
    
    class Meta:
        verbose_name = "Standard Page"
        verbose_name_plural = "Standard Pages"
