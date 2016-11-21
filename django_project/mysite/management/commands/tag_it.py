from django.core.management.base import BaseCommand, CommandError
from django_project.mysite.views import set_tags


class Command(BaseCommand):
    help = 'Set tags for non tagged future events'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        class Request(object):
            GET = {'task': 'empty_future'}

        result = set_tags(Request)
        if result:
            self.stdout.write(self.style.SUCCESS('Successfully tagged. \n %s' % result))
        else:
            self.stdout.write(self.style.ERROR('Tagged ERROR!!!'))