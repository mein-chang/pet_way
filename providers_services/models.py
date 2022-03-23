from django.db import models
import uuid


class ProviderService(models.Model):
    SERVICE_TYPES = (
        ('Pet sitter', 'Pet sitter'),
        ('Pet walker', 'Pet walker'),
        ('Pet trainer', 'Pet trainer'),
        ('Pet taxi', 'Pet taxi'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=11, choices=SERVICE_TYPES)
    price = models.FloatField()
    description = models.TextField()
    provider = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='services')


    def save(self, *args, **kwargs):
            self.full_clean()
            super().save()
            