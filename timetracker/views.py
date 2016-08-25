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
        if self.request.user.is_active:
            serializer.save(user=self.request.user)

        # create session if it doesn't exist
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        session_key = self.request.session.session_key

        self.logger.debug("Creating activity for anonymous user with session "
                          "id: %s", session_key)

        serializer.save(session=session_key)
