from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.models import Page
import uuid6

from apps.core.models import BasePage


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class FormPage(BasePage, AbstractEmailForm):
    template = "pages/form_page.html"
    landing_page_template = "pages/form_page_landing.html"
    subpage_types = []

    uuid = models.UUIDField(default=uuid6.uuid7, editable=False, unique=True)
    intro = models.TextField(blank=True, help_text="Introduction text for the form")
    thank_you_text = models.TextField(
        blank=True, help_text="Text to display after form submission"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("to_address"),
        FieldPanel("from_address"),
        FieldPanel("subject"),
    ]

    def get_form_fields(self):
        return self.form_fields.all()

    def get_data_fields(self):
        data_fields = [
            ("submit_time", "Submission date"),
        ]
        for field in self.get_form_fields():
            data_fields.append((field.clean_name, field.label))
        return data_fields

    def get_url_parts(self, *args, **kwargs):
        """
        Override the get_url_parts method to use the UUID in the URL.
        """
        url_parts = super().get_url_parts(*args, **kwargs)
        if url_parts is None:
            return None

        # Replace the page ID with the UUID
        site_id, root_url, page_path = url_parts
        return (site_id, root_url, f"/{self.uuid.hex}/{page_path}")
