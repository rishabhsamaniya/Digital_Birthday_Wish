from django.urls import path
from . import views

app_name = "wishes"

urlpatterns = [
    path("<slug:slug>/wish/", views.wish_page, name="wish_page"),
]
