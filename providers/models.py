from django.db import models


class Provider(models.Model):
    instagram = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    description = models.TextField()

    # user = models.OneToOneField('users.User', on_delete=models.CASCADE)
