import logging

from rest_framework import viewsets

from timetracker import models, serializers


class ActivityViewSet(viewsets.ModelViewSet):
    """View set for viewing and editing `Activity` instances."""
    serializer_class = serializers.ActivitySerializer

    def __init__(self, *args, **kwargs):
        """Create a logger for the instance."""
        super(ActivityViewSet, self).__init__(*args, **kwargs)

        self.logger = kwargs.pop('logger', logging.getLogger(__name__))

    def get_queryset(self):
        """Retrieve the list of activities to act on.

        Returns:
            QuerySet:
                A `QuerySet` containing the list of `Activity` instances
                owned by the user making the current request.
        """
        q = models.Activity.objects.all()

        if self.request.user.is_active:
            return q.filter(user=self.request.user)

        return q.filter(session=self.request.session.session_key)

    def perform_create(self, serializer):
        """Associate the current user with the created activity."""
        serializer.save(user=self.request.user)
