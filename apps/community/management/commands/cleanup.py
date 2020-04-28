from django.core.management.base import BaseCommand, CommandError
from datetime import datetime as dt

from community import models

from log import get_log

log = get_log('cleanup-ipaccess')

class Command(BaseCommand):
    help = 'clean up ip access table'

    def add_arguments(self, parser):
        parser.add_argument('--all', type=bool, default=False, help="cleanup all data of this table include today's records")

    def handle(self, *args, **options):
        if options['all']:
            r = models.IPAccess.objects.filter().delete()
            log.info(f'clean up all: {r}')
        else:
            r = models.IPAccess.objects.filter(date__lt=dt.now().date()).delete()
            log.info(f'clean up: {r}')
