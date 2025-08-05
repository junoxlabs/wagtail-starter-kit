from django.shortcuts import render
from django.views.generic import DetailView
from .models import FormPage


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
        self.object = self.get_object()
        form = self.object.get_form(
            request.POST, request.FILES, page=self.object, user=request.user
        )

        if form.is_valid():
            self.object.process_form_submission(form)
            # For HTMX, we can return just the thank you content,
            # which can be swapped into the target element.
            return render(
                request,
                self.object.landing_page_template,
                {"page": self.object},
            )

        context = self.get_context_data(form=form)
        return self.render_to_response(context)
