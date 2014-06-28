from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Sends weekly newsletter'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        from _newdaily import send_newsletter
        send_newsletter('Monthly')