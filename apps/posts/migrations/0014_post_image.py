# Generated by Django 4.2 on 2024-10-25 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0013_followtag"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, upload_to="images/"),
        ),
    ]