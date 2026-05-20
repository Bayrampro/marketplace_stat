from django.urls import path

from . import views


app_name = "infographics"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/download/", views.download, name="download"),
]
