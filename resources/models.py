from django.db import models
from core.models import Center

# Create your models here.


class ResourceEntity(models.Model):
    STATUS_CHOICES = [
        ('available', 'Still available'),
        ('unavailable', 'Not available'),
    ]
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Center, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    class Meta:
        abstract = True
    
    def modify_name(self, new_name):
        self.name = new_name
        self.save()

    def modify_location(self, new_location):
        self.location = new_location
        self.save()
    
    def modify_status(self, new_status):
        self.status = new_status
        self.save()
    
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(ResourceEntity):
    tags = models.ManyToManyField(Tag, blank=True)
    
    def modify_tags(self, new_tags):
        self.tags.set(new_tags)
        self.save()
    
    def __str__(self):
        return self.name


