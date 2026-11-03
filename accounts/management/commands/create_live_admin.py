import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create TOMOTO live admin once"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("TOMOTO_ADMIN_USERNAME")
        email = os.environ.get("TOMOTO_ADMIN_EMAIL", "")
        password = os.environ.get("TOMOTO_ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING("Admin environment variables missing.")
            )
            return

        existing = User.objects.filter(username=username).first()

        if existing:
            if not existing.is_superuser:
                raise CommandError(
                    "Username already exists. Choose another admin username."
                )

            self.stdout.write("Admin already exists. No changes made.")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS("Admin created successfully!")
        )