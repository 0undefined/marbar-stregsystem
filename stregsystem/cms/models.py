from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone


def get_active_marbar():
    active = None

    # Get latest marbar with date_start prior to now
    marbars = Marbar.objects.filter(date_start__lt=timezone.now()).order_by('-date_start').first()

    # Get next marbar with date_start later than now
    upcoming_marbar = Marbar.objects.filter(date_start__gt=timezone.now()).order_by('-date_start').first()

    if (marbars.date_end > timezone.now()):
        active = marbars
    elif (upcoming_marbar is not None):
        active = upcoming_marbar

    return active


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


# Køkkener/aspiranter/crew etc.
class MarbarConsumer(models.Model):
    name    = models.CharField(max_length=64, unique=True, blank=False)


# aka. Streger
class MarbarCounter(models.Model):
    counter  = models.IntegerField(default=0)
    marbar   = models.ForeignKey(Marbar,         on_delete=models.CASCADE)
    consumer = models.ForeignKey(MarbarConsumer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-marbar', '-counter']
