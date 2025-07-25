from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


def get_active_marbar():
    active = None

    # Get latest marbar with date_start prior to now
    marbars = Marbar.objects.filter(date_start__lt=timezone.now()).order_by('-date_start').first()

    # Get next marbar with date_start later than now
    upcoming_marbar = Marbar.objects.filter(date_start__gt=timezone.now()).order_by('-date_start').first()

    # Give a 12 hour post-marbar buffer zone to get the glory
    dt = timedelta(hours=12)

    if (marbars is not None and marbars.date_end + dt > timezone.now()):
        active = marbars
    elif (upcoming_marbar is not None):
        active = upcoming_marbar

    return active


# Create your models here.
class Marbar(models.Model):
    title       = models.CharField(max_length=512, default='')
    date_start  = models.DateTimeField('Starting date')
    duration    = models.DurationField(default=timedelta(hours=100))
    extra_hours = models.DurationField(default=timedelta())
    note        = models.TextField(default='', blank=True)
    style       = models.TextField(default='', blank=True)
    banner      = models.ImageField(null=True, blank=True, upload_to='banners')

    elfsight_apikey = models.CharField(max_length=128, null=True, blank=True)

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


class MarbarParticipant(models.Model):
    # The role determines where they are put on the scoreboard
    class Role(models.IntegerChoices):
        DISABLED = 0, "Disabled"
        SECONDARY = 1, "Secondary"
        MAIN = 2, "Main"

    role   = models.IntegerField(choices=Role.choices, default=Role.DISABLED)
    marbar = models.ForeignKey(Marbar, on_delete=models.CASCADE, related_name='participants')
    user   = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def default_participation(marbar, user):
        from stregsystem.settings import DEFAULT_CONSUMERS

        participation = MarbarParticipant.objects.filter(marbar=marbar, user=user)
        if len(participation) == 1:
            return participation[0].role

        username = user.username

        if username in ('Aspiranter', 'Crew', 'Marbarudvalget'):
            return MarbarParticipant.Role.MAIN.value
        elif username in DEFAULT_CONSUMERS:
            return MarbarParticipant.Role.SECONDARY.value
        else:
            return MarbarParticipant.Role.DISABLED.value



# Køkkener/aspiranter/crew etc.
# Bliver automatisk lavet når systemet starter i ./apps.py ud fra listen
# stregsystem.settings.DEFAULT_CONSUMERS
class MarbarConsumer(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)


# New "streger" model, wip
class MarbarScore(models.Model):
    marbar   = models.ForeignKey(Marbar,         on_delete=models.CASCADE)
    consumer = models.ForeignKey(MarbarConsumer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


# aka. Streger
class MarbarCounter(models.Model):
    counter  = models.IntegerField(default=0)
    marbar   = models.ForeignKey(Marbar,         on_delete=models.CASCADE)
    consumer = models.ForeignKey(MarbarConsumer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-marbar', '-counter']
