from django.db import models
import uuid

class Order(models.Model):
    service_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
