import logging

from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory

from timetracker import models


def create_activity(user=None, title='Test Title', start_time=None,
                    end_time=None, logger=None):
    """Create an `Activity` instance for testing purposes.

    The fields are given default values so that instances can be easily
    created for testing purposes.

    Args:
        user (User,optional):
            The user to associate the activity with. If one is not
            provided, a new user is created.
        title (str,optional):
            The title of the activity.
        start_time (datetime,optional):
            The time the activity started. Defaults to the current time
            if not provided.
        end_time (datetime,optional):
            The time the activity ended. Defaults to `None` if not
            provided.

    Returns:
        Activity: An `Activity` instance with the given parameters.
    """
    logger = logger or logging.getLogger(__name__)

    kwargs = {
        'title': title,
    }

    if user is None:
        user = create_user()
    kwargs['user'] = user

    if start_time is not None:
        kwargs['start_time'] = start_time

    if end_time is not None:
        kwargs['end_time'] = end_time

    logger.debug("Creating new test activity with params title: %s, "
                 "start_time: %s, end_time: %s", title, start_time, end_time)

    return models.Activity.objects.create(**kwargs)


def create_user(username=None, password='password', email=None, logger=None):
    """Create a user for testing.

    If the username is already in use, the user with that username is
    retrieved and returned.

    Args:
        username (str,optional):
            The username for the new user. Defaults to 'user' with a
            number appended to it if that name is not available.
        password (str,optional):
            The password for the new user. Defaults to 'password'.d
        email (str,optional):
            The email for the new user. Defaults to
            `<username>@example.com`.
        logger (logger,optional):
            The logger to use for the function. If one is not provided,
            the logger for the current module is retrieved and used.

    Returns:
        User: A `User` instance with the given attributes.
    """
    logger = logger or logging.getLogger(__name__)

    if username is None:
        logger.debug("Generating username.")

        base_name = 'user'
        username = base_name
        suffix = 2

        while get_user_model().objects.filter(username=username).exists():
            username = '{}{}'.format(base_name, suffix)

            suffix += 1

        logger.debug("Using username: %s", username)

    else:
        q = get_user_model().objects.filter(username=username)

        if q.exists():
            return q.get()

    if email is None:
        email = '{}@example.com'.format(username)

        logger.debug("Generated email address: %s", email)

    return get_user_model().objects.create_user(
        username=username, password=password, email=email)
