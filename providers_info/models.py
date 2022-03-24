from django.db import models
import uuid


class ProviderInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instagram = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    description = models.TextField()
    provider = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='provider_info')
