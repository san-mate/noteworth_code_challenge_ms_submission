from urllib3 import PoolManager
from urllib3.util.retry import Retry

from django.conf import settings


class BaseImportBackend(object):
    SITE_URL = None

    def __init__(self):
        self.retry_strategy = Retry(
            total=settings.MAX_API_RETRY,
            status_forcelist=[408, 500, 502, 503, 504])
        self.http = PoolManager(retries=self.retry_strategy)

    def authenticate(self):
        raise NotImplementedError('Implement in subclass')

    def get_auth_header(self, **kwargs):
        raise NotImplementedError('Implement in subclass')

    def get_clinicians(self, **kwargs):
        raise NotImplementedError('Implement in subclass')

    def map_to_model_fields(self, api_object):
        raise NotImplementedError('Implement in subclass')
