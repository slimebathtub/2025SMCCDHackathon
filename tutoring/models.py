from django.db import models
WEEK_DAYS_LIST = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
# Create your models here.
class TutoringDailySchedule(models.Model):
    WEEKDAYS = [(d, d) for d in WEEK_DAYS_LIST]
    
    weekday  = models.CharField(max_length=9, choices=WEEKDAYS, default="Monday")
    subject  = models.CharField(max_length=100, default="Math")
    courses  = models.JSONField(default=list)
    time     = models.CharField(max_length=100, default="None")
    location = models.CharField(max_length=50, default="CSM")
    tutors   = models.CharField(max_length=40, default="None")

    def __str__(self):
        return f"{self.weekday}: {self.subject} - {self.courses} at {self.location} ({self.time})"