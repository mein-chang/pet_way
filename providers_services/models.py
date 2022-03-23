from django.db import models
import uuid


class ProviderService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    provider = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='services')
