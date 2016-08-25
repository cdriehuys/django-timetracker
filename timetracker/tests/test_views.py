from datetime import timedelta

from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from timetracker import models, serializers, views
from timetracker.testing_utils import create_activity, create_user


class TestActivityDetailView(APITestCase):
    """Test cases for the activity detail view.

    This view is part of `ActivityViewSet`.
    """

    def test_delete(self):
        """Test deleting an `Activity` instance.

        Sending a DELETE request to the instance's detail view should
        delete the instance.
        """
        activity = create_activity()

        url = reverse('activity-detail', kwargs={'pk': activity.pk})
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, models.Activity.objects.count())

    def test_get(self):
        """Test getting an `Activity` instances detail view.

        If a GET request is sent to the instance's detail view, the
        instance should be serialized and returned.
        """
        activity = create_activity()
        serializer = serializers.ActivitySerializer(activity)

        url = reverse('activity-detail', kwargs={'pk': activity.pk})
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_invalid_pk(self):
        """Test passing an invalid pk to the activity detail view.

        If no `Activity` instance has the given pk, the view should
        return a 404 status code.
        """
        url = reverse('activity-detail', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_partial_update(self):
        """Test partially updating an `Activity` instance.

        Partial updates should be allowed by sending a PATCH request to
        the instance's detail view.
        """
        activity = create_activity()
        data = {
            'start_time': activity.start_time - timedelta(hours=1)
        }

        url = reverse('activity-detail', kwargs={'pk': activity.pk})
        response = self.client.patch(url, data)

        activity.refresh_from_db()
        serializer = serializers.ActivitySerializer(activity)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(data['start_time'], activity.start_time)

    def test_update(self):
        """Test updating an `Activity` instance.

        Sending a PUT request to the instance's detail view should
        update the instance with the provided data.
        """
        activity = create_activity()
        serializer = serializers.ActivitySerializer(activity)

        data = serializer.data
        data['title'] = 'New Title'
        del data['end_time']

        url = reverse('activity-detail', kwargs={'pk': activity.pk})
        response = self.client.put(url, data)

        activity.refresh_from_db()
        serializer = serializers.ActivitySerializer(activity)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(data['title'], activity.title)


class TestActivityListView(APITestCase):
    """Test cases for the Activity list view."""
    url = reverse('activity-list')

    def test_activities(self):
        """Test the view with activities.

        If there are activites, the view should return a serialized list
        of those activities.
        """
        activity1 = create_activity(title='A1')
        activity2 = create_activity(title='A2')

        serializer = serializers.ActivitySerializer(
            [activity1, activity2], many=True)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_create(self):
        """Test creating a new `Activity` instance.

        Sending a POST request to the list view should create a new
        `Activity` instance with the provided data.
        """
        user = create_user()
        data = {
            'title': 'My Title',
            'start_time': (timezone.now() - timedelta(hours=1)).isoformat(),
            'end_time': timezone.now().isoformat(),
        }

        response = self.client.post(self.url, data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data['title'], response.data['title'])
        self.assertEqual(data['start_time'], response.data['start_time'])
        self.assertEqual(data['end_time'], response.data['end_time'])

    def test_multiple_users(self):
        """Test having activites created by different users.

        Users should only be able to see the activities they've created.
        """
        user1 = create_user()
        user2 = create_user()

        self.client.force_login(user=user1)

        activity = create_activity(user=user1)
        create_activity(user=user2, title="Not User 1's Activity")

        serializer = serializers.ActivitySerializer([activity], many=True)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_no_activites(self):
        """Test the view with no activities.

        If there are no `Activity` instances, an empty list should be
        returned.
        """
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)
