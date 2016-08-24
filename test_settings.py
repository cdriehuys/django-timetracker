"""Settings for testing the app.

This means that the settings are as stripped down as possible.
"""

SECRET_KEY = 'secret'

INSTALLED_APPS = (
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    # Third party apps
    'django_nose',
    'rest_framework',

    # Custom apps
    'timetracker',
)


# Since we're only using the database for tests, we can make it in
# memory to speed up the tests.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ROOT_URLCONF = 'test_urls'
