from django.core.management.base import BaseCommand, CommandError

from authentication.models import User


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **kwargs):
        email = "admin@example.com"
        password = "admin"

        try:
            if User.objects.filter(email=email).exists():
                raise CommandError("A user with this email already exists.")

            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS("Successfully created superuser"))
        except Exception as e:
            raise CommandError(f"Error creating superuser: {e}")
