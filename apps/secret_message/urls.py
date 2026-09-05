from django.urls import path
from . import views

app_name = "secret_message"

urlpatterns = [
    path("<slug:slug>/secret/", views.secret_message_reveal, name="reveal"),
]
