import json
from hashlib import sha256

from providers.backends.base import BaseImportBackend
from providers.models import ProviderToken


class NoteworthImportBackend(BaseImportBackend):
    SITE_URL = 'http://localhost:5000'
    API_FIELDS_TO_MODEL = {
        'name_given': 'first_name',
        'name_family': 'last_name',
        'title': 'title',
        'clinic': 'clinic_name'
    }

    def authenticate(self):
        auth_response = self.http.request('GET', self.SITE_URL + '/auth')
        token = auth_response.headers.get('Super-Secure-Token', None)
        if not token:
            raise Exception('No token provided')
        ProviderToken.objects.update_or_create(
            provider_site=self.SITE_URL,
            defaults={'token': token}
        )

    def get_auth_header(self, **kwargs):
        path = kwargs['path']
        provider_token = ProviderToken.objects.filter(provider_site=self.SITE_URL)
        header = {}
        if provider_token.exists():
            provider_token = provider_token.get()
            checksum = "{}{}".format(provider_token.token, path)
            auth_header = sha256(checksum.encode('utf-8')).hexdigest()
            header['X-Request-Checksum'] = auth_header
        return header

    def get_clinicians(self, retries=None, **kwargs):
        path = '/providers'
        headers = self.get_auth_header(path=path)
        if not retries:
            retries = self.retry_strategy
        providers_response = self.http.request(
            'GET',
            self.SITE_URL + path,
            headers=headers,
            retries=retries)
        try:
            json_response = json.loads(providers_response.data.decode('utf8'))
            return json_response['providers']
        except json.decoder.JSONDecodeError:
            new_retry = retries.increment()
            return self.get_clinicians(new_retry)

    def map_to_model_fields(self, api_object):
        matched_fields = set(api_object.keys()) & set(self.API_FIELDS_TO_MODEL.keys())
        return {self.API_FIELDS_TO_MODEL[field_name]: api_object[field_name] for field_name in matched_fields}
