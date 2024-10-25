# Generated by Django 5.1.2 on 2024-10-20 09:28

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField()),
            ],
            options={
                "verbose_name": "Страна",
                "verbose_name_plural": "Страны",
            },
        ),
    ]
