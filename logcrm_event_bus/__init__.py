"""Define Flask and Celery app and the necessary tasks."""
from datetime import datetime
import json
import logging

from celery import Celery, Task
from moflask.flask import BaseApp
from mohawk import Sender
from raven.contrib.flask import Sentry
import raven.contrib.celery as raven_celery
import requests


class App(BaseApp):
    """Flask app object used for configuration management and commands."""

    def __init__(self, *args, **kwargs):
        """Initialize the Flask App object."""
        super().__init__('logcrm_event_bus', *args, **kwargs)
        self.celery = self.init_celery()

    def init_celery(self):
        """Create a new celery instance add configure it."""
        celery = Celery('logcrm_event_bus')
        celery.conf.update(self.config)
        self.register_tasks(celery)
        return celery

    def register_tasks(self, celery):
        """Register celery tasks for all configured API key."""
        for name, key in self.config['API_KEYS'].items():
            key.setdefault('url', self.config['LOGCRM_URL'])
            key.setdefault('timeout', self.config.get('LOGCRM_TIMEOUT', 20))
            key.setdefault('algorithm', 'sha256')
            task = LogcrmSendTask(name, key)
            celery.tasks.register(task)

    def init_sentry(self):
        """Set up sentry as error and logging handler.

        Use of sentry is enforced for this app.
        """
        self.sentry = Sentry(self)
        raven_celery.register_logger_signal(self.sentry.client)
        raven_celery.register_signal(self.sentry.client)


class LogcrmSendTask(Task):
    """Celery task to send a logcrm event using a specific API-key."""

    task_name_prefix = 'logcrm_event_bus.send_event.'
    retry_backoff = True

    def __init__(self, task_name, key):
        """Create new logcrm event task.

        Args:
            task_name (str): Machine name for this API-key.
            key (dict): logCRM connection data.
        """
        self.name = self.task_name_prefix + task_name
        self.url = key['url']
        self.timeout = key['timeout']
        self.credentials = {
            'id': key['public_key'],
            'key': key['secret_key'],
            'algorithm': key['algorithm'],
        }
        self.logger = logging.getLogger('logcrm_event_bus')
        self.logger.debug('Initialized logcrm: %s.', self.url,
                          extra={'public_key': key['public_key']})

    def run(self, event, *args, **kwargs):  # pylint: disable=arguments-differ
        """Send an event to logcrm using a post request.

        Args:
            event (dict): Data to send to logCRM.
        """
        event.setdefault('date', datetime.utcnow().isoformat())
        content_type = 'application/json'
        data = json.dumps(event)
        sender = Sender(self.credentials, self.url, 'POST', content=data,
                        content_type=content_type)
        headers = {
            'Authorization': sender.request_header,
            'Content-Type': content_type,
        }
        response = requests.post(self.url, data=data, headers=headers)
        response.raise_for_status()
