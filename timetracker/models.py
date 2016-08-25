"""Models for the `timetracker` app.

These models are responsible for storing and representing the data that
is manipulated within the app.
"""
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class Activity(models.Model):
    """An activity with a title, start time, and end time."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True)
    session = models.CharField(max_length=40, blank=True, null=True)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        """Create a logger for the instance."""
        super(Activity, self).__init__(*args, **kwargs)

        self.logger = kwargs.pop('logger', logging.getLogger(__name__))

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

    def save(self, *args, **kwargs):
        """Validate and save the instance to the database.

        Ensures that only one of `user` or `session` is specified.

        Raises:
            ValidationError:
                if both `user` and `session` are not `None`.
        """
        if self.user is not None and self.session is not None:
            self.logger.error("Tried to create Activity with both `user` and "
                              "`session` specified.")

            raise ValidationError("Only one of `user` or `session` may be "
                                  "specified.")

        return super(Activity, self).save(*args, **kwargs)
