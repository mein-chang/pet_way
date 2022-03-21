from django.db import models
import uuid


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()

    # Relacionamento 1:N com o Provider:
    # provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, related_name='services')
