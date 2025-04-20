from django.db import models

# Create your models here.
class TutoringDailySchedule(models.Model):
    WEEKDAYS = [
        ('Monday',    "Monday"),
        ('Tuesday',   "Tuesday"),
        ('Wednesday', "Wednesday"),
        ('Thursday',  "Thursday"),
        ('Friday',    "Friday"),
    ]

    weekday  = models.CharField(max_length=9, choices=WEEKDAYS, default="Monday")
    subject  = models.CharField(max_length=100, default="Math")
    courses  = models.CharField(max_length=70)
    time     = models.CharField(max_length=100)
    location = models.CharField(max_length=50, default="MRC")

    def __str__(self):
        return f"{self.weekday}: {self.subject} − {self.courses} at {self.location} ({self.time})"