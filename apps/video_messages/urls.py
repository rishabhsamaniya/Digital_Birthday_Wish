from django.urls import path
from . import views

app_name = "video_messages"

urlpatterns = [
    path("<slug:slug>/messages/", views.video_messages_showcase, name="messages"),
]
