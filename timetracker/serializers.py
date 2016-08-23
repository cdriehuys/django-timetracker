from rest_framework import serializers

from timetracker import models


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for the `Activity` model."""

    class Meta(object):
        """Options for the `ActivitySerializer`."""
        fields = ('id', 'title', 'start_time', 'end_time')
        model = models.Activity
