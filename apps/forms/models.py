from django.db import models
from django.core.mail import send_mail
from django.template.response import TemplateResponse
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_flexible_forms.models import (
    StreamFormMixin,
    AbstractSessionFormSubmission,
    AbstractSubmissionRevision,
)

from apps.core.models import BasePage
from apps.blocks.models import ContentStreamBlock
from wagtail_flexible_forms.blocks import FormFieldsBlock


class SubmissionRevision(AbstractSubmissionRevision):
    pass


class FormSubmission(AbstractSessionFormSubmission):
    page = ParentalKey(
        "FormPage", on_delete=models.CASCADE, related_name="form_submissions"
    )

    @staticmethod
    def get_revision_class():
        return SubmissionRevision


class FormPage(StreamFormMixin, BasePage):
    template = "pages/form_page.html"
    landing_page_template = "pages/form_page_landing.html"
    subpage_types = []

    body = StreamField(
        ContentStreamBlock(),
        use_json_field=True,
        blank=True,
    )
    thank_you_text = models.TextField(
        blank=True, help_text="Text to display after form submission"
    )
    form_fields = StreamField(
        FormFieldsBlock(),
        use_json_field=True,
        blank=True,
    )
    to_address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional - email address to send submissions to",
    )
    from_address = models.CharField(max_length=255, blank=True)
    subject = models.CharField(max_length=255, blank=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("body"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("to_address"),
        FieldPanel("from_address"),
        FieldPanel("subject"),
    ]

    def get_session_submission_class(self):
        return FormSubmission

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if request.htmx:
            context["base_template"] = "_partial.html"
        else:
            context["base_template"] = "base.html"
        return context

    def process_form_submission(self, form):
        submission = self.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=self,
        )
        if self.to_address:
            self.send_mail(form)
        return submission

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(",")]
        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ", ".join(value)
            content.append(f"{field.label}: {value}")
        content = "\n".join(content)
        send_mail(self.subject, content, self.from_address, addresses)
