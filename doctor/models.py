from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from authentication.models import MyUser

from common.models import BaseModelWithUid

from .choices import DoctorStatus


class Department(BaseModelWithUid):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class Achievement(BaseModelWithUid):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=600)
    year = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"UID: {self.uid}, {self.name}"


class Degree(BaseModelWithUid):
    name = models.CharField(max_length=300)
    institute = models.CharField(max_length=300, blank=True)
    result = models.CharField(max_length=255, blank=True)
    passing_year = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Name: {self.name}"


class Doctor(BaseModelWithUid):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name="doctors"
    )
    secondary_phone = PhoneNumberField(blank=True)
    secondary_email = models.EmailField(blank=True)
    department = models.ForeignKey(Department, models.SET_NULL, blank=True, null=True)
    experience = models.IntegerField()
    appointment_fee = models.DecimalField(
        max_digits=10, null=True, blank=True, decimal_places=2, default=0
    )
    consultation_fee = models.DecimalField(
        max_digits=10, null=True, blank=True, decimal_places=2, default=0
    )
    follow_up_fee = models.DecimalField(
        max_digits=10, null=True, blank=True, decimal_places=2, default=0
    )
    check_up_fee = models.DecimalField(
        max_digits=10, null=True, blank=True, decimal_places=2, default=0
    )
    status = models.CharField(
        max_length=20,
        choices=DoctorStatus.choices,
        db_index=True,
        default=DoctorStatus.ACTIVE,
    )

    def __str__(self):
        return f"UID: {self.uid}"
