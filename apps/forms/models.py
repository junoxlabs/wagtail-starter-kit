from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import StreamField
from wagtail.models import Page
import uuid6

from apps.core.models import BasePage
from apps.blocks.models import BaseStreamBlock


class FormField(AbstractFormField):
    page = models.ForeignKey(
        "FormPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class FormPage(BasePage, AbstractEmailForm):
    template = "pages/form_page.html"
    landing_page_template = "pages/form_page_landing.html"
    subpage_types = []

    uuid = models.UUIDField(default=uuid6.uuid7, editable=False, unique=True)
    intro = models.TextField(blank=True, help_text="Introduction text for the form")
    thank_you_text = models.TextField(
        blank=True, help_text="Text to display after form submission"
    )

    form_fields_streamblock = StreamField(
        BaseStreamBlock(),
        use_json_field=True,
        blank=True,
        help_text="Build your form by adding form fields",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("form_fields_streamblock"),
        FieldPanel("thank_you_text"),
        FieldPanel("to_address"),
        FieldPanel("from_address"),
        FieldPanel("subject"),
    ]

    def get_form_fields(self):
        return self.form_fields_streamblock

    def get_data_fields(self):
        data_fields = [
            ("submit_time", "Submission date"),
        ]
        for field in self.get_form_fields():
            data_fields.append((field.block.name, field.value.get("label")))
        return data_fields

    def get_url_parts(self, *args, **kwargs):
        """
        Override the get_url_parts method to use the UUID in the URL.
        """
        url_parts = super().get_url_parts(*args, **kwargs)
        if url_parts is None:
            return None

        # Replace the page ID with the UUID
        url_parts = list(url_parts)
        url_parts[1] = self.uuid.hex
        return url_parts

    @classmethod
    def get_page_from_path(cls, path):
        """
        Override get_page_from_path to resolve pages by UUID.
        """
        try:
            uuid_obj = uuid6.UUID(path.strip("/"))
            return cls.objects.get(uuid=uuid_obj)
        except (ValueError, cls.DoesNotExist):
            return None
