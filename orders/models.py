from django.db import models
import uuid

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
