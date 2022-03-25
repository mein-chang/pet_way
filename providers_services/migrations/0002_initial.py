# Generated by Django 4.0.3 on 2022-03-24 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('providers_services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='providerservice',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL),
        ),
    ]