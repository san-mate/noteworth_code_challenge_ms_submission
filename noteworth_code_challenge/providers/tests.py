from django.test import TestCase

from providers.backends.noteworth_challenge import NoteworthImportBackend


class NoteworthImportBackendTestCase(TestCase):
    def setUp(self):
        self.backend = NoteworthImportBackend()

    def test_auth_endpoint_error_response(self):
        pass

    def test_auth_header_not_present_on_response(self):
        pass

    def test_provider_endpoint_error_response(self):
        pass

    def test_provider_incomplete_content(self):
        pass

    def test_clinician_mapping_when_missing_field(self):
        pass

    def test_provider_endpoint_with_invalid_token(self):
        pass


class ImportCommandTestCase(TestCase):

    def test_command_finishes_with_valid_backend(self):
        pass
