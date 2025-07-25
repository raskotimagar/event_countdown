from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def status(self):
        now = timezone.now()
        if self.event_date <= now:
            return "expired"
        return "upcoming"