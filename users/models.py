from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Airports(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6,unique = True, validators=[alphanumeric])
    createdBy = models.CharField(max_length=255)