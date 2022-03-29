from django.db import models
import uuid
# Create your models here.


class PetAdoption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    available = models.BooleanField(default=True)
    castrated = models.BooleanField()
    is_vaccinated = models.BooleanField()
    is_health = models.BooleanField()
    additional_info = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)
    adopted_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey('users.User', related_name='pets_adoptions', on_delete=models.CASCADE)
    pet = models.OneToOneField('pets.Pet', on_delete=models.CASCADE, related_name='pet_adoption')