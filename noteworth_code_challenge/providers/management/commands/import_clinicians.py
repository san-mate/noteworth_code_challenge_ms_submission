from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports all Clinicians from the Noteworth Callenge API'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
