from django.db import models
import uuid
# Create your models here.

class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    specie = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    gender = models.CharField(max_length=125)
    size = models.CharField(max_length=155)
    date_joined = models.DateTimeField(auto_now_add=True)