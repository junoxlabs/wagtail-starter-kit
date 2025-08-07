from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Testimonial(models.Model):
    """
    A snippet for customer testimonials.
    """

    quote = models.TextField(help_text="The testimonial quote.")
    author = models.CharField(
        max_length=255, help_text="The author of the testimonial."
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="An optional image of the author.",
    )

    panels = [
        FieldPanel("quote"),
        FieldPanel("author"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return f'"{self.quote}" - {self.author}'

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"


@register_snippet
class TeamMember(models.Model):
    """
    A snippet for team member profiles.
    """

    name = models.CharField(max_length=255, help_text="The name of the team member.")
    role = models.CharField(max_length=255, help_text="The role of the team member.")
    photo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="A photo of the team member.",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("photo"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"


@register_snippet
class Faq(models.Model):
    """
    A snippet for frequently asked questions.
    """

    question = models.CharField(max_length=255, help_text="The question.")
    answer = models.TextField(help_text="The answer.")
    
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("pricing", "Pricing"),
        ("technical", "Technical"),
    ]
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="general",
        help_text="Category for the FAQ",
    )

    panels = [
        FieldPanel("question"),
        FieldPanel("answer"),
        FieldPanel("category"),
    ]

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


@register_snippet
class Cta(models.Model):
    """
    A reusable call-to-action snippet.
    """
    
    title = models.CharField(max_length=256, help_text="The title of the Cta.")
    description = models.TextField(help_text="A brief description for the Cta.")
    button_text = models.CharField(max_length=256, help_text="Text for the button.")
    button_url = models.URLField(help_text="URL for the button.")
    
    style = models.CharField(
        max_length=50,
        choices=[
            ("primary", "Primary"),
            ("secondary", "Secondary"),
            ("cta", "CTA"),
            ("button", "Button"),
            ("link", "Link"),
        ],
        default="primary",
        help_text="Style variant for the Cta",
    )
    
    header_script = models.TextField(
        blank=True,
        null=True,
        help_text="Additional script to inject in the header when this CTA is used."
    )
    
    footer_script = models.TextField(
        blank=True,
        null=True,
        help_text="Additional script to inject in the footer when this CTA is used."
    )
    
    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("button_text"),
        FieldPanel("button_url"),
        FieldPanel("style"),
        FieldPanel("header_script"),
        FieldPanel("footer_script"),
    ]
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Reusable CTA"
        verbose_name_plural = "Reusable CTAs"


