from django.db import models

from resources.models import ResourceEntity

# Create your models here.
class Room(ResourceEntity):
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

    