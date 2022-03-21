from email.policy import default
from django.db import models
import uuid

class Rating(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,default=False)
    
    customer_rating = models.IntegerField()
    customer_comment = models.TextField(default="")
    
    provider_rating = models.IntegerField()
    provider_comment = models.TextField(default="")
    
