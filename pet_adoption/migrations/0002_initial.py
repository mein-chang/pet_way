# Generated by Django 4.0.3 on 2022-03-29 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pets', '0001_initial'),
        ('pet_adoption', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='petadoption',
            name='pet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pet_adoption', to='pets.pet'),
        ),
    ]
