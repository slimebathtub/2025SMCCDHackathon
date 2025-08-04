from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Center(models.Model):
    # basic information
    center_full_name = models.CharField(max_length=255)
    center_short_name = models.CharField(max_length=50)
    center_building_address = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def __repr__(self):
        return f'{self.center_full_name} at {self.center_building_address} by {self.user.username}'

    def __eq__(self, other):
        return isinstance(other, Center) and self.center_full_name == other.center_full_name

    def __hash__(self):
        return hash(self.center_full_name)