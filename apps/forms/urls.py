from django.urls import path
from .views import FormPageView

app_name = "forms"

urlpatterns = [
    path("<uuid:uuid>/", FormPageView.as_view(), name="form_page"),
]