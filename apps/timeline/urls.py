from django.urls import path
from . import views

app_name = "timeline"

urlpatterns = [
    path("<slug:slug>/timeline/", views.timeline_journey, name="journey"),
]
