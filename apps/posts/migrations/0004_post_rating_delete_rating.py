# Generated by Django 5.1.2 on 2024-10-24 10:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0003_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="rating",
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name="Rating",
        ),
    ]
