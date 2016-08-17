import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from timetracker import models, serializers


@api_view(['GET'])
def activity_list_view(request, logger=None):
    """Return a list of activities."""
    logger = logger or logging.getLogger(__name__)

    activities = models.Activity.objects.all()

    logger.debug("Listing %d activities", activities.count())

    serializer = serializers.ActivitySerializer(activities, many=True)

    return Response(serializer.data)
