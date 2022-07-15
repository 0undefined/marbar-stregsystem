from django.db import models
from datetime import timedelta

# Create your models here.
class Marbar(models.Model):
    date_start = models.DateTimeField('Starting date')
    #date_end   = models.DateTimeField('Ending date')
    duration   = models.DurationField(default=timedelta(days=3))
    title      = models.CharField(max_length=512, default="")
    note       = models.TextField(default="")
