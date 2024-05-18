from django.core.management.base import BaseCommand
from appname.models import Main

class Command(BaseCommand):
    help = 'Increment days field of Main model'

    def handle(self, *args, **kwargs):
        mains = Main.objects.all()
        for main in mains:
            main.days = str(int(main.days) + 1)
            main.save()
        self.stdout.write(self.style.SUCCESS('Successfully incremented days for all Main instances'))
