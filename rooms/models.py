from django.db import models

from resources.models import ResourceEntity

# Create your models here.
class Room(ResourceEntity):
    people_available = models.IntegerField()

    