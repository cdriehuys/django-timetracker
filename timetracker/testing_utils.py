import logging

from timetracker import models


def create_activity(title='Test Title', start_time=None, end_time=None,
                    logger=None):
    """Create an `Activity` instance for testing purposes.

    The fields are given default values so that instances can be easily
    created for testing purposes.

    Args:
        title (str): The title of the activity.
        start_time (datetime,optional): The time the activity started.
            Defaults to the current time if not provided.
        end_time (datetime,optional): The time the activity ended.
            Defaults to `None` if not provided.

    Returns:
        Activity: An `Activity` instance with the given parameters.
    """
    logger = logger or logging.getLogger(__name__)

    kwargs = {
        'title': title,
    }

    if start_time is not None:
        kwargs['start_time'] = start_time

    if end_time is not None:
        kwargs['end_time'] = end_time

    logger.debug("Creating new test activity with params title: %s, "
                 "start_time: %s, end_time: %s", title, start_time, end_time)

    return models.Activity.objects.create(**kwargs)
