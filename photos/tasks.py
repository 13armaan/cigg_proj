from celery import shared_task
from PIL import Image, ExifTags
from django.core.files.base import ContentFile
from io import BytesIO

from .models import Photo
from django.conf import settings
import os
@shared_task
def generate_thumbnail(photo_id):
    photo = Photo.objects.get(photo_id=photo_id)

    base_img = Image.open(photo.original_img)
    
    # Extract EXIF metadata
    exif_data = {}
    try:
        raw_exif = base_img.getexif()
        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                # Ignore byte data which cannot be serialized to JSON
                if isinstance(value, bytes):
                    continue
                # Cast tuples/custom objects to string
                if isinstance(value, (int, float, str, bool)):
                    exif_data[tag] = value
                else:
                    exif_data[tag] = str(value)
    except Exception:
        pass

    photo.metadata = exif_data

    #if we have png or other img type

    if base_img.mode in ("RGBA", "P"):
        base_img = base_img.convert("RGB")


    # resize (keep aspect ratio)
    base_img.thumbnail((300, 300))

    buffer = BytesIO()
    base_img.save(buffer, format="JPEG")
    buffer.seek(0)

    thumbnail_name = f"thumb_{photo.photo_id}.jpg"

    photo.thumbnail_img.save(
        thumbnail_name,
        ContentFile(buffer.read()),
        save=False
    )

    photo.is_processed = True
    photo.save()
    return photo_id

from celery import shared_task
from django.db import transaction
from .models import Photo, Tag


@shared_task(queue="ml")
def auto_tag_photo(photo_id):
    # imported inside ML worker for compatibility with the venv_ml
    import numpy as np # type: ignore
    from tensorflow.keras.applications.efficientnet_v2 import ( # type: ignore
        EfficientNetV2B3,
        preprocess_input,
        decode_predictions
    )
    from tensorflow.keras.preprocessing import image # type: ignore

    # Load model lazily (cached per worker process)
    if not hasattr(auto_tag_photo, "model"):
        auto_tag_photo.model = EfficientNetV2B3(weights="imagenet")

    model = auto_tag_photo.model

    try:
        photo = Photo.objects.get(photo_id=photo_id)
    except Photo.DoesNotExist:
        return "Photo not found"

    with photo.original_img.open('rb') as f:
        img = image.load_img(BytesIO(f.read()), target_size=(300, 300))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)
    decoded = decode_predictions(preds, top=5)[0]

    
    for _, label, confidence in decoded:
        tag, _ = Tag.objects.get_or_create(name=label)
        photo.tags.add(tag)

    return [label for _, label, _ in decoded]
