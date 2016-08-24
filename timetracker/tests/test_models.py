from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

import mock

from timetracker import models
from timetracker.testing_utils import create_activity, create_user


class TestActivityModel(TestCase):
    """Test cases for the `Activity` model."""

    def test_creation(self):
        """Test creating an instance of the `Activity` model.

        The instance's constructor should accept `start_time`,
        `end_time`, and `title` parameters.
        """
        user = create_user()
        title = 'Test Activity'
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=1)

        activity = models.Activity.objects.create(
            user=user,
            title='Test Activity',
            start_time=start_time,
            end_time=end_time)

        self.assertEqual(title, activity.title)
        self.assertEqual(start_time, activity.start_time)
        self.assertEqual(end_time, activity.end_time)

    def test_creation_defaults(self):
        """Test the defaults for the `Activity` model.

        By default, `start_time` should be the current time, and
        `end_time` should be `None`.
        """
        user = create_user()
        title = 'Test Activity'
        time = timezone.now()
        field = models.Activity._meta.get_field('start_time')

        with mock.patch.object(field, 'default', autospec=True,
                               side_effect=lambda: time) as mock_now:
            activity = models.Activity.objects.create(user=user, title=title)

        self.assertEqual(1, mock_now.call_count)
        self.assertEqual(time, activity.start_time)
        self.assertIsNone(activity.end_time)

    def test_get_absolute_url(self):
        """Test getting the absolute url of an `Activity` instance.

        The returned URL should be the instance's detail view.
        """
        activity = create_activity()
        expected = reverse('activity-detail', kwargs={'pk': activity.pk})

        self.assertEqual(expected, activity.get_absolute_url())

    def test_is_active(self):
        """Test the `Activity` model's `is_active` property.

        An `Activity` with no `end_time` is active, but if it has an
        `end_time` it is not active.
        """
        title = 'Test Activity'

        activity = models.Activity(user=create_user(), title=title)

        self.assertTrue(activity.is_active)

        activity.end_time = timezone.now()

        self.assertFalse(activity.is_active)

    def test_string_conversion_with_end_time(self):
        """Test converting an `Activity` instance to a string.

        If an `Activity` instance has an `end_time`, then its string
        conversion should return a string in the form:
        "<title>: <start_time> - <end_time>"

        The times should be formatted as YYYY-MM-DD HH:MM
        """
        title = 'Test Activity'
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=3)

        expected = '{}: {} - {}'.format(
            title,
            start_time.strftime('%Y-%M-%d %H:%m'),
            end_time.strftime('%Y-%M-%d %H:%m'))

        activity = models.Activity(
            user=create_user(),
            title=title,
            start_time=start_time,
            end_time=end_time)

        self.assertEqual(expected, str(activity))

    def test_string_conversion_without_end_time(self):
        """Test string conversion without an end time.

        If an `Activity` instance doesn't have an `end_time`, then its
        string conversion should return a string in the form:
        "<title>: <start_time> - (in progress)"

        The start time should be formatted as YYYY-MM-DD HH:MM
        """
        title = 'Test Activity'
        start_time = timezone.now()

        expected = '{}: {} - (in progress)'.format(
            title, start_time.strftime('%Y-%M-%d %H:%m'))

        activity = models.Activity(
            user=create_user(), title=title, start_time=start_time)

        self.assertEqual(expected, str(activity))
