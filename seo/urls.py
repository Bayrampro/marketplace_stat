from django.urls import path

from . import views


app_name = "seo"

urlpatterns = [
    path("", views.index, name="index"),
]
