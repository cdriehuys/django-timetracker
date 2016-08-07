"""Settings for testing the app.

This means that the settings are as stripped down as possible.
"""

SECRET_KEY = 'secret'

INSTALLED_APPS = (
    # Third party apps
    'django_nose',

    # Custom apps
    'timetracker',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
