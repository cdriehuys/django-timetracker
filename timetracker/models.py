"""Models for the `timetracker` app.

These models are responsible for storing and representing the data that
is manipulated within the app.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


def _default_user():
    """Get a default user to allow for migrations."""
    return get_user_model().objects.create_user(username='DEFAULT_USER').id


class Activity(models.Model):
    """An activity with a title, start time, and end time."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=_default_user)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Convert the instance to a string.

        Returns:
            str: A string in the format
                "`title`: `start_time` - `end_time`", where the dates
                are formatted like YYYY-MM-DD HH:MM.
        """
        if self.end_time:
            end_str = self.end_time.strftime('%Y-%M-%d %H:%m')
        else:
            end_str = '(in progress)'

        return '{}: {} - {}'.format(
            self.title, self.start_time.strftime('%Y-%M-%d %H:%m'), end_str)

    def get_absolute_url(self):
        """Return the URL of the instance's detail view.

        Returns:
            str: The URL of the instance's detail view, in the format:
                `/activities/<pk>/`.
        """
        return reverse('activity-detail', kwargs={'pk': self.pk})

    @property
    def is_active(self):
        """bool: True if the instance has no `end_time`, False
            otherwise.
        """
        return self.end_time is None
