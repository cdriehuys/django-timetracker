from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

import mock

from timetracker import models


class TestActivityModel(TestCase):
    """Test cases for the `Activity` model."""

    def test_creation(self):
        """Test creating an instance of the `Activity` model.

        The instance's constructor should accept `start_time`,
        `end_time`, and `title` parameters.
        """
        title = 'Test Activity'
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=1)

        activity = models.Activity.objects.create(
            title='Test Activity', start_time=start_time, end_time=end_time)

        self.assertEqual(title, activity.title)
        self.assertEqual(start_time, activity.start_time)
        self.assertEqual(end_time, activity.end_time)

    def test_creation_defaults(self):
        """Test the defaults for the `Activity` model.

        By default, `start_time` should be the current time, and
        `end_time` should be `None`.
        """
        title = 'Test Activity'
        time = timezone.now()
        field = models.Activity._meta.get_field('start_time')

        with mock.patch.object(field, 'default', autospec=True,
                               side_effect=lambda: time) as mock_now:
            activity = models.Activity.objects.create(title=title)

        self.assertEqual(1, mock_now.call_count)
        self.assertEqual(time, activity.start_time)
        self.assertIsNone(activity.end_time)
