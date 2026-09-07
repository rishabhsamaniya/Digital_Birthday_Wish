import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


MAX_IMAGE_DIMENSION = 2000
JPEG_QUALITY = 82


def optimize_image_field(field_file):
    """Resize and compress an uploaded image before it is stored."""
    if not field_file or not getattr(field_file, "file", None):
        return

    try:
        field_file.file.seek(0)
        with Image.open(field_file.file) as source:
            image = ImageOps.exif_transpose(source)
            image.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), Image.Resampling.LANCZOS)
            if image.mode not in ("RGB", "L"):
                background = Image.new("RGB", image.size, "white")
                if "A" in image.getbands():
                    background.paste(image, mask=image.getchannel("A"))
                else:
                    background.paste(image)
                image = background
            else:
                image = image.convert("RGB")

            output = BytesIO()
            image.save(output, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
            output.seek(0)
            filename = os.path.splitext(os.path.basename(field_file.name))[0] + ".jpg"
            field_file.save(filename, ContentFile(output.read()), save=False)
    except (OSError, ValueError):
        field_file.file.seek(0)
