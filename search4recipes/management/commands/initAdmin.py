import os
from django.core.management import BaseCommand
from search4recipes.models import User


class Command(BaseCommand):
    help = 'Dodadaje superużytkownika do bazy'

    def handle(self, *args, **options):
        try:
            if User.objects.count() == 0:
                email = os.environ['SUPER_EMAIL']
                password = os.environ['SUPER_PASSWORD']
                username = os.environ['SUPER_USERNAME']
                print('Tworzenie użytkownika administracyjnego %s.' % username)
                User.objects.create_superuser(username=username, email=email, password=password)
            else:
                print('Konto administratora może zostać stworzone jedynie, gdy inne konta nie istnieją.')
        except KeyError:
            print('Brak którejś z wymaganych zmiennych środowiskowych: SUPER_EMAIL, SUPER_PASSWORD, SUPER_USERNAME.')
