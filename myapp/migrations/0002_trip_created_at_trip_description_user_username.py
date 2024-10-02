# Generated by Django 5.1.1 on 2024-09-23 20:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trip",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="trip",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(default="default_user", max_length=100),
        ),
    ]
