from django.core.management.base import BaseCommand, CommandError
from django_project.mysite.views import update_event


class Command(BaseCommand):
    help = 'Add all confidence event to mysite_events (approve or reject)'

    def add_arguments(self, parser):
        parser.add_argument('events_list', nargs='*', type=int)

    def handle(self, *args, **options):
        result = update_event(options['events_list'])
        if result['status'] == 'Success':
            self.stdout.write(self.style.SUCCESS('Success. \n %s' % result))
        else:
            self.stdout.write(self.style.ERROR('update_event ERROR!!!'))