from django.db import models
import uuid

from users.models import User


class Address(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    zip_code = models.CharField(max_length=9)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    complement = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    users = models.ManyToManyField(
        User, related_name="addresses", through='addresses.UserAddress')


class UserAddress(models.Model):
    address = models.ForeignKey('addresses.Address', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
