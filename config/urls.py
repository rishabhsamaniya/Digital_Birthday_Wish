from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = "apps.profiles.views.custom_404_view"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("", include("apps.landing.urls", namespace="landing")),
    path("", include("apps.memories.urls", namespace="memories")),
    path("", include("apps.timeline.urls", namespace="timeline")),
    path("", include("apps.love_notes.urls", namespace="love_notes")),
    path("", include("apps.gallery.urls", namespace="gallery")),
    path("", include("apps.music.urls", namespace="music")),
    path("", include("apps.video_messages.urls", namespace="video_messages")),
    path("", include("apps.secret_message.urls", namespace="secret_message")),
    path("", include("apps.wishes.urls", namespace="wishes")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    # Dynamic Profile URLs (e.g. /priya/, /sneha/)
    path("", include("apps.profiles.urls", namespace="profiles")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
