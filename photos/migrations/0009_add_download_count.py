from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("photos", "0008_alter_photo_album"),
    ]

    operations = [
        migrations.AddField(
            model_name="photo",
            name="download_count",
            field=models.IntegerField(default=0),
        ),
    ]
