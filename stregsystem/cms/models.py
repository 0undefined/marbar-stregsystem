from datetime import timedelta

from django.db import models

# Create your models here.
class Marbar(models.Model):
    date_start = models.DateTimeField('Starting date')
    duration   = models.DurationField(default=timedelta(days=3))
    title      = models.CharField(max_length=512, default="")
    note       = models.TextField(default="")
    style      = models.TextField(default="")
