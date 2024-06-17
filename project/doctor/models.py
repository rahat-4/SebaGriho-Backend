from django.db import models

from authentication.models import User

from common.models import BaseModelWithUid

from .choices import AffiliationStatus, DoctorStatus


class LanguageSpoken(BaseModelWithUid):
    language = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Language: {self.language}"


class Department(BaseModelWithUid):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class Specialty(BaseModelWithUid):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

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


class Affiliation(BaseModelWithUid):
    title = models.CharField(max_length=250, blank=True)
    hospital_name = models.CharField(max_length=250, blank=True)
    status = models.CharField(
        max_length=20,
        choices=AffiliationStatus.choices,
        db_index=True,
        default=AffiliationStatus.CURRENT,
    )

    def __str__(self):
        return f"UID: {self.uid}, Title: {self.title}"


class Doctor(BaseModelWithUid):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctors")
    about = models.TextField(blank=True)
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


class DoctorAdditionalConnector(BaseModelWithUid):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="additional_connectors"
    )
    specialty = models.ManyToManyField(
        Specialty, blank=True, related_name="doctor_specialties"
    )
    degree = models.ManyToManyField(Degree, blank=True, related_name="doctor_degrees")
    achievement = models.ManyToManyField(
        Achievement, blank=True, related_name="doctor_achievements"
    )
    affiliation = models.ManyToManyField(
        Affiliation, blank=True, related_name="doctor_affiliations"
    )
    language_spoken = models.ManyToManyField(
        LanguageSpoken, blank=True, related_name="doctor_languages"
    )
