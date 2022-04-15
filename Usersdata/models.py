from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
# Create your models here.


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
class User(AbstractUser):
    
    first_name=models.CharField(max_length=150, validators=[alphanumeric])
    last_name = models.CharField(max_length=150, validators=[alphanumeric])
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = PhoneNumberField(unique=True)
    username=None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []