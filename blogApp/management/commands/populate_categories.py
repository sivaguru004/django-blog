from blogApp.models import Catagory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "this Commands insert Catagories Data"
    # delete exist data

    def handle(self, *args, **options):
         
        Catagory.objects.all().delete()

        catagories = ['Sports', 'Technologies', 'Science', 'Art', 'Food']

        for c in catagories:
            Catagory.objects.create(name = c)

        self.stdout.write(self.style.SUCCESS("Complited inserting data!"))