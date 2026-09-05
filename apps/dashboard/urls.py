from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.dashboard_login, name="login"),
    path("logout/", views.dashboard_logout, name="logout"),
    path("", views.dashboard_index, name="index"),
    path("profiles/", views.profile_list, name="profile_list"),
    path("profiles/create/", views.profile_create, name="profile_create"),
    path("profiles/<int:pk>/edit/", views.profile_edit, name="profile_edit"),
    path("profiles/<int:pk>/delete/", views.profile_delete, name="profile_delete"),
    path("profiles/<int:pk>/toggle-status/", views.profile_toggle_status, name="profile_toggle_status"),
    path("profiles/<int:pk>/qr/", views.profile_qr, name="profile_qr"),
    
    # Memory CRUD
    path("profiles/<int:profile_id>/memories/", views.memory_list, name="memory_list"),
    path("profiles/<int:profile_id>/memories/create/", views.memory_create, name="memory_create"),
    path("memories/<int:pk>/edit/", views.memory_edit, name="memory_edit"),
    path("memories/<int:pk>/delete/", views.memory_delete, name="memory_delete"),

    # Timeline CRUD
    path("profiles/<int:profile_id>/timeline/", views.timeline_list, name="timeline_list"),
    path("profiles/<int:profile_id>/timeline/create/", views.timeline_create, name="timeline_create"),
    path("timeline/<int:pk>/edit/", views.timeline_edit, name="timeline_edit"),
    path("timeline/<int:pk>/delete/", views.timeline_delete, name="timeline_delete"),

    # Love Notes CRUD
    path("profiles/<int:profile_id>/love-notes/", views.love_note_list, name="love_note_list"),
    path("profiles/<int:profile_id>/love-notes/create/", views.love_note_create, name="love_note_create"),
    path("love-notes/<int:pk>/edit/", views.love_note_edit, name="love_note_edit"),
    path("love-notes/<int:pk>/delete/", views.love_note_delete, name="love_note_delete"),

    # Gallery CRUD
    path("profiles/<int:profile_id>/gallery/", views.gallery_list, name="gallery_list"),
    path("profiles/<int:profile_id>/gallery/create/", views.gallery_create, name="gallery_create"),
    path("gallery/<int:pk>/edit/", views.gallery_edit, name="gallery_edit"),
    path("gallery/<int:pk>/delete/", views.gallery_delete, name="gallery_delete"),

    # Music CRUD
    path("profiles/<int:profile_id>/music/", views.music_list, name="music_list"),
    path("profiles/<int:profile_id>/music/create/", views.music_create, name="music_create"),
    path("music/<int:pk>/edit/", views.music_edit, name="music_edit"),
    path("music/<int:pk>/delete/", views.music_delete, name="music_delete"),

    # Video Messages CRUD
    path("profiles/<int:profile_id>/videos/", views.video_list, name="video_list"),
    path("profiles/<int:profile_id>/videos/create/", views.video_create, name="video_create"),
    path("videos/<int:pk>/edit/", views.video_edit, name="video_edit"),
    path("videos/<int:pk>/delete/", views.video_delete, name="video_delete"),

    # Secret Message CRUD
    path("profiles/<int:profile_id>/secret/", views.secret_message_detail, name="secret_message_detail"),
    path("secret/<int:pk>/delete/", views.secret_message_delete, name="secret_message_delete"),

    # Wishes Submissions Management
    path("profiles/<int:profile_id>/wishes/", views.wish_list, name="wish_list"),
    path("wishes/<int:pk>/toggle-approval/", views.wish_toggle_approval, name="wish_toggle_approval"),
    path("wishes/<int:pk>/delete/", views.wish_delete, name="wish_delete"),
]
