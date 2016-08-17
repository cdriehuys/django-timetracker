from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from timetracker import models, serializers
from timetracker.testing_utils import create_activity


class TestActivitySerializer(TestCase):
    """Test cases for the activity serializer."""

    def test_deserialize(self):
        """Test deserializing an activity.

        Passing valid data to the serializer should allow an `Activity`
        instance to be constructed by the serializer.
        """
        title = 'Test Activity'
        end_time = timezone.now()
        start_time = end_time - timedelta(hours=3)

        data = {
            'title': title,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
        }

        serializer = serializers.ActivitySerializer(data=data)

        self.assertTrue(serializer.is_valid())

        activity = serializer.save()

        self.assertEqual(1, models.Activity.objects.count())
        self.assertEqual(title, activity.title)
        self.assertEqual(start_time, activity.start_time)
        self.assertEqual(end_time, activity.end_time)

    def test_readonly_fields(self):
        """Test trying to write to readonly fields.

        Trying to write to a readonly field should have no effect.
        """
        data = {
            'id': -4382,
            'title': 'Test Activity',
        }

        serializer = serializers.ActivitySerializer(data=data)

        self.assertTrue(serializer.is_valid())

        activity = serializer.save()

        self.assertEqual(data['title'], activity.title)
        self.assertNotEqual(data['id'], activity.id)

    def test_serialize_all(self):
        """Test serializing all the fields from an `Activity` instance.

        Each field should be serialized into a string representation,
        and those should be combined into a JSON representation of the
        `Activity` instance.
        """
        end_time = timezone.now()
        start_time = end_time - timedelta(hours=1)
        activity = create_activity(start_time=start_time, end_time=end_time)

        expected = {
            'id': activity.id,
            'title': activity.title,
            'start_time': activity.start_time.isoformat(),
            'end_time': activity.end_time.isoformat(),
        }

        serializer = serializers.ActivitySerializer(activity)

        self.assertEqual(expected, serializer.data)
