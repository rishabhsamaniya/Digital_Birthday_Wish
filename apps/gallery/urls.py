from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path("<slug:slug>/gallery/", views.gallery_showcase, name="showcase"),
]
