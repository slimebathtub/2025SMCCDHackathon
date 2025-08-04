from django.db import models
from core.models import Center
WEEK_DAYS_LIST = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
# Create your models here.
class TutoringDailySchedule(models.Model):
    WEEKDAYS = [(d, d) for d in WEEK_DAYS_LIST]
    
    weekday  = models.CharField(max_length=9, choices=WEEKDAYS, default="Monday", db_index=True)
    subject  = models.CharField(max_length=100, default="Math", db_index=True)
    courses  = models.CharField(max_length=100, default="Empty")
    time     = models.CharField(max_length=100, default="None")
    tutors   = models.CharField(max_length=40, default="None")
    location = models.ForeignKey(Center, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=["weekday", "subject"]),  # composite for the common joint filter
        ]
    
    @property
    def full_name(self):
        return self.location.center_full_name if self.location else ""

    def __str__(self):
        return f'Schedule Unit on {self.weekday} for {self.full_name}'

    def __repr__(self):
        return f"{self.weekday}: {self.subject} - {self.courses} at {self.full_name}, ({self.time}) with tutors {self.tutors}"