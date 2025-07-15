from django.urls import path

from .views import RunPromptView


urlpatterns = [path("run/", RunPromptView.as_view(), name="run_prompt")]
