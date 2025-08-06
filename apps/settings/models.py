from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.models import Orderable


class SocialMediaLink(Orderable):
    settings = ParentalKey("SiteSettings", related_name="social_media_links")
    platform = models.CharField(max_length=255, help_text="e.g. 'Facebook', 'Twitter', 'LinkedIn'")
    url = models.URLField()
    icon = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel("platform"),
        FieldPanel("url"),
        FieldPanel("icon"),
    ]

@register_setting
class SiteSettings(BaseSiteSetting, ClusterableModel):
    """
    Site settings for the marketing starter kit.
    """
    site_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The site title"
    )
    site_description = models.TextField(
        blank=True,
        null=True,
        help_text="The site description"
    )
    site_logo = models.ForeignKey(
        Image,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Site logo"
    )

    contact_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Contact email address"
    )
    contact_phone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Physical address"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('site_title'),
                FieldPanel('site_description'),
                FieldPanel('site_logo'),
            ],
            heading="Site Identity"
        ),
        MultiFieldPanel(
            [
                FieldPanel('contact_email'),
                FieldPanel('contact_phone'),
                FieldPanel('address'),
            ],
            heading="Contact Information"
        ),
        MultiFieldPanel(
            [
                InlinePanel("social_media_links", label="Social Media Link"),
            ],
            heading="Social Media"
        ),
    ]

    class Meta:
        verbose_name = "Site Settings"
