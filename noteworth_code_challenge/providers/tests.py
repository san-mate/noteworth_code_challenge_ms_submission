from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
import httpretty
from urllib3.exceptions import MaxRetryError

from providers.backends.noteworth_challenge import NoteworthImportBackend


@override_settings(MAX_API_RETRY=0)
@httpretty.activate
class NoteworthImportBackendTestCase(TestCase):
    def setUp(self):
        self.backend = NoteworthImportBackend()

    def test_auth_endpoint_error_response(self):
        with self.subTest('Test api call to /auth getting a 500'):
            httpretty.register_uri(
                httpretty.GET,
                self.backend.SITE_URL + '/auth',
                status=500,
            )
            self.assertRaises(MaxRetryError, self.backend.authenticate)

        with self.subTest('Test api call to /auth getting a 408'):
            httpretty.register_uri(
                httpretty.GET,
                self.backend.SITE_URL + '/auth',
                status=408
            )
            self.assertRaises(MaxRetryError, self.backend.authenticate)

    def test_auth_header_not_present_on_response(self):
        httpretty.register_uri(
            httpretty.GET,
            self.backend.SITE_URL + '/auth',
            status=200
        )
        with self.assertRaises(Exception) as context:
            self.backend.authenticate()

        self.assertEquals('No token provided', str(context.exception))

    def test_provider_endpoint_error_response(self):
        with self.subTest('Test api call to /auth getting a 500'):
            httpretty.register_uri(
                httpretty.GET,
                self.backend.SITE_URL + '/providers',
                status=500
            )
            self.assertRaises(MaxRetryError, self.backend.get_clinicians)

        with self.subTest('Test api call to /auth getting a 408'):
            httpretty.register_uri(
                httpretty.GET,
                self.backend.SITE_URL + '/providers',
                status=408
            )
            self.assertRaises(MaxRetryError, self.backend.get_clinicians)

    def test_provider_incomplete_content(self):
        httpretty.register_uri(
            httpretty.GET,
            self.backend.SITE_URL + '/providers',
            status=200,
            body='{"incomplete_json',
        )
        self.assertRaises(MaxRetryError, self.backend.get_clinicians)

    def test_clinician_mapping_when_missing_field(self):
        clinician = {
            'name_given': 'Martin',
            'title': 'Dr',
            'clinic': 'Big Clinic'
        }
        expected_clinician = {
            'first_name': 'Martin',
            'title': 'Dr',
            'clinic_name': 'Big Clinic'
        }
        mapped_clinician = self.backend.map_to_model_fields(clinician)
        self.assertEquals(mapped_clinician, expected_clinician)

    def test_provider_endpoint_with_invalid_token(self):
        pass


@override_settings(MAX_API_RETRY=0)
@httpretty.activate
class ImportCommandTestCase(TestCase):

    def test_command_finishes_with_valid_backend(self):
        backend = NoteworthImportBackend()
        httpretty.register_uri(
            httpretty.GET,
            backend.SITE_URL + '/auth',
            status=200,
            super_secure_token='123',
        )
        httpretty.register_uri(
            httpretty.GET,
            backend.SITE_URL + '/providers',
            status=200,
            body='{"providers":[]}',
        )

        out = StringIO()
        call_command('import_clinicians', 'noteworth_challenge_api', stdout=out)
        self.assertIn('Finished', out.getvalue())
