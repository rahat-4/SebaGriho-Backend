from django.db import models

from authentication.models import User
from common.models import BaseModelWithUid

from .choices import PatientStatus


class Patient(BaseModelWithUid):
    status = models.CharField(
        max_length=50,
        choices=PatientStatus.choices,
        default=PatientStatus.ACTIVE,
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patients")

    def __str__(self):
        return f"UID: {self.uid}"
