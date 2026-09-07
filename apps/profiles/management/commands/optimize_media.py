from django.core.management.base import BaseCommand

from apps.gallery.models import GalleryPhoto
from apps.memories.models import Memory
from apps.media_utils import optimize_image_field
from apps.profiles.models import BirthdayProfile
from apps.timeline.models import TimelineEvent
from apps.video_messages.models import VideoMessage


class Command(BaseCommand):
    help = "Resize and compress existing uploaded images."

    def handle(self, *args, **options):
        targets = (
            (BirthdayProfile, "profile_image"),
            (BirthdayProfile, "hero_image"),
            (BirthdayProfile, "cover_image"),
            (GalleryPhoto, "image"),
            (Memory, "image"),
            (TimelineEvent, "image"),
            (VideoMessage, "thumbnail"),
        )
        optimized = 0
        for model, field_name in targets:
            for instance in model.objects.exclude(**{f"{field_name}__exact": ""}).iterator():
                field = getattr(instance, field_name)
                if not field:
                    continue
                old_name = field.name
                optimize_image_field(field)
                if field.name != old_name:
                    instance.save(update_fields=[field_name, "updated_at"])
                    field.storage.delete(old_name)
                    optimized += 1
        self.stdout.write(self.style.SUCCESS(f"Optimized {optimized} media files."))
