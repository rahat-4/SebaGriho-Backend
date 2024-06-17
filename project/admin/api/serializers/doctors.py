from django.contrib.auth import get_user_model

from rest_framework import serializers

from doctor.models import (
    Achievement,
    Affiliation,
    Degree,
    Department,
    Doctor,
    DoctorAdditionalConnector,
    Specialty,
    LanguageSpoken,
)

User = get_user_model()
