from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Center(models.Model):
    # basic information
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=128)
    center_full_name = models.CharField(max_length=255)
    center_short_name = models.CharField(max_length=50)
    center_building_address = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name