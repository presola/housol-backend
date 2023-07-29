
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
"""
   User class for extending the Django default user to allow for additional fields 
   and modification of existing fields
"""
class User(AbstractUser):
    email = models.EmailField(unique=True)
