from django.core.management.base import BaseCommand, CommandError
from menu.fsa_api import FSAAPI


class Command(BaseCommand):
    args = 'Entity type'

    def handle(self, *args, **options):
        fsa_obj = FSAAPI()
        if not len(args):
            raise CommandError('Entity type not provided.')
        fsa_obj.process(args[0])
