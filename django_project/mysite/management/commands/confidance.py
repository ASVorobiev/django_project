from django.core.management.base import BaseCommand, CommandError
from django_project.mysite.views import push_confidence


class Command(BaseCommand):
    help = 'Add all confidence event to mysite_events (approve or reject)'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        result = push_confidence()
        if result:
            self.stdout.write(self.style.SUCCESS('Success. \n %s' % result))
        else:
            self.stdout.write(self.style.ERROR('Confidence ERROR!!!'))