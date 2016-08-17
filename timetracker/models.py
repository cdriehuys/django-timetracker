"""Models for the `timetracker` app.

These models are responsible for storing and representing the data that
is manipulated within the app.
"""

from django.db import models
from django.utils import timezone


class Activity(models.Model):
    """An activity with a title, start time, and end time."""
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)
