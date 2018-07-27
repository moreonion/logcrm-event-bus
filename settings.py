"""Settings for the logcrm_event_bus app."""


class TestingConfig:  # pylint: disable=too-few-public-methods
    """Configuration used when running automated tests."""

    LOGCRM_URL = 'http://dev-null'
    API_KEYS = {
        'test_key': {
            'public_key': 'pk_private-key',
            'secret_key': 'sk_secret-key',
        }
    }
    BROKER_URL = 'memory://localhost'
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTION = True
    SENTRY_DSN = 'http://user:pass@dev-null/42'
