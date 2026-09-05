from django.urls import path
from . import views

app_name = "love_notes"

urlpatterns = [
    path("<slug:slug>/love-notes/", views.love_notes_journey, name="notes"),
]
