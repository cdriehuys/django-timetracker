from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework import status

from timetracker import serializers, views
from timetracker.testing_utils import RequestTestMixin, create_activity


class TestActivityListView(RequestTestMixin, TestCase):
    """Test cases for the Activity list view."""
    url = reverse('activity-list')

    def request_view(self, request):
        """Pass a request to the view for this test case."""
        return views.activity_list_view(request)

    def test_activities(self):
        """Test the view with activities.

        If there are activites, the view should return a serialized list
        of those activities.
        """
        activity1 = create_activity(title='A1')
        activity2 = create_activity(title='A2')

        serializer = serializers.ActivitySerializer(
            [activity1, activity2], many=True)

        request = self.factory.get(self.url)
        response = self.request_view(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_no_activites(self):
        """Test the view with no activities.

        If there are no `Activity` instances, an empty list should be
        returned.
        """
        request = self.factory.get(self.url)
        response = self.request_view(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response.render()

        self.assertEqual([], response.data)
