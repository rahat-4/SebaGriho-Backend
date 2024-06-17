from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Run multiple management commands to generate all credentials."

    def handle(self, *args, **options):
        # Run cleancache command
        self.stdout.write(self.style.SUCCESS("Running cleancache command..."))
        call_command("cleancache")

        # Run makemigrations command
        self.stdout.write(self.style.SUCCESS("Running makemigrations command..."))
        call_command("makemigrations")

        # Run migrate command
        self.stdout.write(self.style.SUCCESS("Running migrate command..."))
        call_command("migrate")

        # Run createsuperuser command
        self.stdout.write(self.style.SUCCESS("Running createsuperuser command..."))
        call_command("create_superuser")

        self.stdout.write(self.style.SUCCESS("All commands executed successfully!"))
