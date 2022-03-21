from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import uuid


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    
    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=False, null=True)
    cpf = models.CharField(max_length=20)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20)
    is_provider = models.BooleanField()
    is_admin = models.BooleanField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'birthdate', 'phone', 'is_provider', 'is_admin', ]

    objects = CustomUserManager()
