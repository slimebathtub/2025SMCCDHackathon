from django.db import models
# Create your models here.

class ClubInfo(models.Model):
    name = models.CharField(max_length=100, default="Math Club")
    #description = models.TextField(default="The best one yet.")
    day = models.CharField(max_length=50, default="Wednesday")
    time = models.CharField(max_length=50, default="1:00 PM - 2:00 PM")
    #meetings = models.CharField(max_length=100, default="Wednesday at 1:00 PM - 2:00 PM")
    location = models.CharField(max_length=100, default="Bldg 18 at 307")
    advisors = models.JSONField(default=list)
    advisors_email = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} on {self.day}, {self.time} at {self.location}"