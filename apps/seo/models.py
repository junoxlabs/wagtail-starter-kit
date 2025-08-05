from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


@register_setting
class SEOSettings(BaseGenericSetting):
    """
    Global SEO settings for the site.
    """
    site_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The site title used in SEO metadata"
    )
    site_description = models.TextField(
        blank=True,
        null=True,
        help_text="The site description used in SEO metadata"
    )
    site_keywords = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated keywords for the site"
    )
    site_logo = models.ForeignKey(
        Image,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Site logo used in SEO metadata"
    )
    site_favicon = models.ForeignKey(
        Image,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Site favicon used in SEO metadata"
    )
    default_socialsharing_image = models.ForeignKey(
        Image,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Default image for social media sharing"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('site_title'),
                FieldPanel('site_description'),
                FieldPanel('site_keywords'),
            ],
            heading="Text Settings"
        ),
        MultiFieldPanel(
            [
                FieldPanel('site_logo'),
                FieldPanel('site_favicon'),
                FieldPanel('default_socialsharing_image'),
            ],
            heading="Image Settings"
        ),
    ]

    class Meta:
        verbose_name = "SEO Settings"
