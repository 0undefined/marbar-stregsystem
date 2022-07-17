from datetime import timedelta

from django.db import models
from django.urls import reverse


# Create your models here.
class Marbar(models.Model):
    title       = models.CharField(max_length=512, default='')
    date_start  = models.DateTimeField('Starting date')
    duration    = models.DurationField(default=timedelta(days=3))
    extra_hours = models.DurationField(default=timedelta())
    note        = models.TextField(default='', blank=True)
    style       = models.TextField(default='', blank=True)
    banner      = models.ImageField(null=True, blank=True, upload_to='banners')

    def get_absolute_url(self):
        return reverse('view', kwargs={'pk': self.id})

    @property
    def date_end(self):
        return self.date_start + self.duration + self.extra_hours

    @property
    def duration_h(self):
        return int(self.duration.total_seconds() / 60 / 60)

    class Meta:
        ordering = ['-date_start']
