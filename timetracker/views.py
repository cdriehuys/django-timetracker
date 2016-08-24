from rest_framework import viewsets

from timetracker import models, serializers


class ActivityViewSet(viewsets.ModelViewSet):
    """View set for viewing and editing `Activity` instances."""
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer

    def perform_create(self, serializer):
        """Associate the current user with the created activity."""
        serializer.save(user=self.request.user)
