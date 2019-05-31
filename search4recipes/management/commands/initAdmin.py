import os
from django.core.management import BaseCommand
from search4recipes.models import User


class Command(BaseCommand):
    help = 'Creates superuser where no users is present in database.'

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            email = os.environ['SUPER_EMAIL']
            password = os.environ['SUPER_PASSWORD']
            username = os.environ['SUPER_USERNAME']
            print('Tworzenie użytkownika administracyjnego %s.' % username)
            User.objects.create_superuser(username=username, email=email, password=password)
        else:
            print('Konto administratora może zostać stworzone jedynie, gdy inne konta nie istnieją.')
