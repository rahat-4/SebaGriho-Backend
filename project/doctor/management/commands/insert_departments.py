import json
from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import Department


class Command(BaseCommand):
    help = "Insert departments and sub-departments into the database from a JSON file"

    def handle(self, *args, **options):
        # Path to the JSON file
        json_file_path = (
            settings.BASE_DIR / "doctor/management/commands/departments_data.json"
        )

        # Read the JSON file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Process each department
        for dept in data["departments"]:
            parent, created = Department.objects.get_or_create(name=dept["name"])
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created department: {parent.name}")
                )
            else:
                self.stdout.write(f"Department already exists: {parent.name}")

            # Process sub-departments
            for sub_dept in dept.get("sub_departments", []):
                child, created = Department.objects.get_or_create(
                    name=sub_dept, parent=parent
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created sub-department: {child.name} under {parent.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        f"Sub-department already exists: {child.name} under {parent.name}"
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully inserted all departments and sub-departments"
            )
        )
