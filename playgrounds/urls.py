from django.urls import path

from .views import playground_page

urlpatterns = [path("", playground_page, name="playground")]
