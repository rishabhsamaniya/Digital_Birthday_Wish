from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("create/", views.create_wizard, name="create_wizard"),
    path("my-wishes/", views.my_profiles, name="my_profiles"),
    path("<slug:slug>/unlock/", views.profile_password_gate, name="password_gate"),
    path("<slug:slug>/success/", views.creation_success, name="creation_success"),
    path("<slug:slug>/", views.profile_detail, name="detail"),
    path("<slug:slug>/birthday/", views.birthday_reveal, name="birthday_reveal"),
    path("<slug:slug>/countdown/", views.countdown_timer, name="countdown"),
    path("<slug:slug>/card/", views.birthday_card, name="card"),
    path("<slug:slug>/qr/", views.profile_qr_code, name="qr_code"),
    path("<slug:slug>/qr/wish/", views.profile_qr_code_wish, name="qr_code_wish"),
]
