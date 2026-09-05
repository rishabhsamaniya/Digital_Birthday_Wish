from django.urls import path
from . import views

app_name = "music"

urlpatterns = [
    path("<slug:slug>/music/", views.music_experience, name="experience"),
]
