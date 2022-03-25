from django.db import models
import uuid
from ratings.models import Rating

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    rating = models.OneToOneField(Rating,null=True,on_delete=models.SET_NULL)
    service = models.ForeignKey('providers_services.ProviderService', null=True, on_delete=models.SET_NULL, related_name='orders')