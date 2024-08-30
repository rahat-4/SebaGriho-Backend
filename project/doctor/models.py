from django.db import models
from django.utils.text import slugify
from authentication.models import User
from common.models import BaseModelWithUid
from .choices import (
    AffiliationStatus,
    DoctorStatus,
    ScheduleStatus,
    ShiftStatus,
    DayStatus,
)


class LanguageSpoken(BaseModelWithUid):
    language = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.language


class Department(BaseModelWithUid):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sub_departments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (UID: {self.uid})"


class Specialty(BaseModelWithUid):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} (UID: {self.uid})"


class Achievement(BaseModelWithUid):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=600)
    year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.year})"


class Degree(BaseModelWithUid):
    name = models.CharField(max_length=300)
    institute = models.CharField(max_length=300, blank=True)
    result = models.CharField(max_length=255, blank=True)
    passing_year = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} from {self.institute} ({self.passing_year})"


class Affiliation(BaseModelWithUid):
    title = models.CharField(max_length=250)
    hospital_name = models.CharField(max_length=250)
    status = models.CharField(
        max_length=20,
        choices=AffiliationStatus.choices,
        db_index=True,
        default=AffiliationStatus.CURRENT,
    )

    def __str__(self):
        return f"{self.title} at {self.hospital_name} ({self.get_status_display()})"


class Doctor(BaseModelWithUid):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    registration_number = models.CharField(max_length=255, unique=True)
    about = models.TextField(blank=True)
    departments = models.ManyToManyField(Department, blank=True, related_name="doctors")
    specialties = models.ManyToManyField(Specialty, blank=True, related_name="doctors")
    experience = models.PositiveIntegerField()
    appointment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    follow_up_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    check_up_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=DoctorStatus.choices,
        db_index=True,
        default=DoctorStatus.ACTIVE,
    )
    degrees = models.ManyToManyField(Degree, blank=True, related_name="doctors")
    achievements = models.ManyToManyField(
        Achievement, blank=True, related_name="doctors"
    )
    affiliations = models.ManyToManyField(
        Affiliation, blank=True, related_name="doctors"
    )
    languages_spoken = models.ManyToManyField(
        LanguageSpoken, blank=True, related_name="doctors"
    )

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} (UID: {self.uid})"

    def get_primary_department(self):
        return self.departments.first()


class DoctorContact(BaseModelWithUid):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="contacts"
    )
    contact_type = models.CharField(max_length=50)  # e.g., 'Phone', 'Email', 'WhatsApp'
    contact_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.contact_type}: {self.contact_value}"


class Schedule(BaseModelWithUid):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="schedules"
    )
    day = models.CharField(max_length=20, choices=DayStatus.choices)
    shift = models.CharField(max_length=20, choices=ShiftStatus.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20, choices=ScheduleStatus.choices, default=ScheduleStatus.ACTIVE
    )

    def __str__(self):
        return f"Dr. {self.doctor.user.get_full_name()} - {self.get_day_display()} {self.get_shift_display()}"

    class Meta:
        unique_together = ("doctor", "day", "shift")
