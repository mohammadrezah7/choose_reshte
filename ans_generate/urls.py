from django.urls import path

from . import views


app_name = "ans_generate"

urlpatterns = [
    path("generate/", views.generate_analysis, name="generate"),
    path("status/", views.analysis_status, name="status"),
]
