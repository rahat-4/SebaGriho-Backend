from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from authentication.models import MyUser
from common.models import BaseModelWithUid

from .choices import PatientStatus


class Patient(BaseModelWithUid):
    secondary_phone = PhoneNumberField(blank=True)
    secondary_email = models.EmailField(blank=True)
    status = models.CharField(
        max_length=50,
        choices=PatientStatus.choices,
        default=PatientStatus.ACTIVE,
    )

    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name="patients"
    )

    def __str__(self):
        return f"UID: {self.uid}"
