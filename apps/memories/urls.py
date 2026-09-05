from django.urls import path
from . import views

app_name = "memories"

urlpatterns = [
    path("<slug:slug>/memories/", views.memory_stories, name="stories"),
]
