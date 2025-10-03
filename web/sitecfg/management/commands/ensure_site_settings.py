from django.core.management.base import BaseCommand
from sitecfg.models import SiteSettings

class Command(BaseCommand):
    help = 'Ensure a single SiteSettings row exists'
    def handle(self, *args, **opts):
        obj = SiteSettings.objects.first() or SiteSettings.objects.create()
        self.stdout.write(self.style.SUCCESS(f'OK: id={obj.id}, site_name={obj.site_name!r}'))