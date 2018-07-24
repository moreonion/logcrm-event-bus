"""Integration test for the logcrm_event_bus app."""

from logcrm_event_bus import App


class TestApp:
    """Integration tests for the app object."""

    app = None

    def setup_method(self, _):
        """Create new app instance for testing."""
        self.app = App(env='Testing')

    def test_test_key_task_registered(self):
        """Test whether the celery task has been registered for the test API-key."""
        assert 'logcrm_event_bus.send_event.test_key' in self.app.celery.tasks
