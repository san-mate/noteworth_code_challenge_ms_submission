from django.core.management.base import BaseCommand, CommandError

from clinicians.models import Clinician
from providers.backends import ALLOWED_IMPORT_BACKENDS


class Command(BaseCommand):
    help = 'Imports all Clinicians from the Noteworth Callenge API'

    def add_arguments(self, parser):
        parser.add_argument(
            'provider',
            choices=ALLOWED_IMPORT_BACKENDS.keys(),
            help='The name of the backend used to pull clinicians'
        )

    def handle(self, *args, **options):
        backend_name = options['provider']
        backend = ALLOWED_IMPORT_BACKENDS[backend_name]()
        self.stdout.write(self.style.WARNING('Authenticating to: %s' % backend.SITE_URL))
        try:
            backend.authenticate()
        except Exception:
            raise CommandError('Unable to authenticate to: %s' % backend.SITE_URL)
        self.stdout.write(self.style.SUCCESS('Successfully authenticated.'))
        self.stdout.write(self.style.WARNING('Retriving clinicians from: %s' % backend.SITE_URL))
        try:
            api_clinicians = backend.get_clinicians()
        except Exception:
            raise CommandError('Unable retrive clinicians from: %s' % backend.SITE_URL)
        self.stdout.write(self.style.SUCCESS('Importing %s clinicians' % len(api_clinicians)))
        for clinician in api_clinicians:
            # Map the API clinician to our model and save it
            new_clinicician, created = Clinician.objects.update_or_create(
                **backend.map_to_model_fields(clinician)
            )
            if created:
                self.stdout.write(self.style.SUCCESS('CREATED: %s' % new_clinicician))
            else:
                self.stdout.write(self.style.SUCCESS('UPDATED: %s' % new_clinicician))
        self.stdout.write(self.style.SUCCESS('Finished.'))
