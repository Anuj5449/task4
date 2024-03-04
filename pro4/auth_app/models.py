from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField



class User(AbstractUser):
    GENDER = [
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'Other')
    ]
    
    ROLES = [
        ('manager', 'manager'),
        ('employee', 'employee'),
        ('developer', 'developer')
    ]
    
    gender   = models.CharField(max_length=6, choices=GENDER, default = 'male')
    address  = models.TextField(blank = True, null = True)
    role     = models.CharField(max_length=10, choices=ROLES, default='manager')
    pincode = models.CharField(max_length= 6, blank = True, null = True)
    city = models.CharField(max_length= 30, blank = True, null = True)
    company = models.CharField(max_length= 50, blank = True, null = True)
    contact = PhoneNumberField(region="IN", blank = True, null = True)
    