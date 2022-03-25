# Generated by Django 4.0.3 on 2022-03-24 14:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer_rating', models.IntegerField()),
                ('customer_comment', models.TextField(default='')),
                ('provider_rating', models.IntegerField()),
                ('provider_comment', models.TextField(default='')),
            ],
        ),
    ]
