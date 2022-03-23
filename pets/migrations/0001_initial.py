# Generated by Django 4.0.3 on 2022-03-23 16:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('birthdate', models.DateField()),
                ('specie', models.CharField(max_length=255)),
                ('breed', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=125)),
                ('size', models.CharField(max_length=155)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
