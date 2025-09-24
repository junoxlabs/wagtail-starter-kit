import logging
from django.shortcuts import render
from django.views.generic import DetailView
from .models import FormPage

logger = logging.getLogger(__name__)


class FormPageView(DetailView):
    model = FormPage
    template_name = "pages/form_page.html"
    context_object_name = "page"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in kwargs:
            context["form"] = self.object.get_form(
                page=self.object, user=self.request.user
            )
        return context

    def post(self, request, *args, **kwargs):
        logger.info("Form submission received")
        self.object = self.get_object()
        form = self.object.get_form(
            request.POST, request.FILES, page=self.object, user=request.user
        )
        logger.info(f"Form is valid: {form.is_valid()}")

        if form.is_valid():
            logger.info("Processing form submission")
            self.object.process_form_submission(form)
            logger.info("Form submission processed successfully")
            # For Turbo, we return the full landing page
            return render(
                request,
                self.object.landing_page_template,
                {"page": self.object, "base_template": "base.html"},
            )
        else:
            logger.info("Form is not valid")
            logger.info(f"Form errors: {form.errors}")

        context = self.get_context_data(form=form)
        return self.render_to_response(context)
