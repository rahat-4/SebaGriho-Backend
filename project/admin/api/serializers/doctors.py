from django.contrib.auth import get_user_model
from django.db import transaction

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

from common.serializers import (
    AchievementSlimSerializer,
    AffiliationSlimSerializer,
    DegreeSlimSerializer,
    DoctorSlimSerializer,
    SpecialtySlimSerializer,
    LanguageSpokenSlimSerializer,
)

User = get_user_model()


class AdminDoctorListSerializer(serializers.ModelSerializer):
    doctor = DoctorSlimSerializer()
    degree = DegreeSlimSerializer(many=True)
    achievement = AchievementSlimSerializer(many=True)
    specialty = SpecialtySlimSerializer(many=True)
    affiliation = AffiliationSlimSerializer(many=True)
    language_spoken = LanguageSpokenSlimSerializer(many=True)

    class Meta:
        model = DoctorAdditionalConnector
        fields = [
            "doctor",
            "degree",
            "achievement",
            "specialty",
            "affiliation",
            "language_spoken",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            doctor_data = validated_data.pop("doctor")
            degrees_data = validated_data.pop("degree", [])
            achievements_data = validated_data.pop("achievement", [])
            specialties_data = validated_data.pop("specialty", [])
            affiliations_data = validated_data.pop("affiliation", [])
            languages_spoken_data = validated_data.pop("language_spoken", [])

            user_data = doctor_data.pop("user")
            department_data = doctor_data.pop("department")

            user = User.objects.create(**user_data)
            department = Department.objects.create(**department_data)

            doctor_instance = Doctor.objects.create(
                user=user, department=department, **doctor_data
            )

            doctor_additional_connector = DoctorAdditionalConnector.objects.create(
                doctor=doctor_instance
            )

            for degree_data in degrees_data:
                degree_instance, _ = Degree.objects.get_or_create(**degree_data)
                doctor_additional_connector.degree.add(degree_instance)

            for achievement_data in achievements_data:
                achievement_instance, _ = Achievement.objects.get_or_create(
                    **achievement_data
                )
                doctor_additional_connector.achievement.add(achievement_instance)

            for specialty_data in specialties_data:
                department_data = specialty_data.pop("department")
                department_instance, _ = Department.objects.get_or_create(
                    **department_data
                )
                specialty_instance, _ = Specialty.objects.get_or_create(
                    department=department_instance, **specialty_data
                )
                doctor_additional_connector.specialty.add(specialty_instance)

            for affiliation_data in affiliations_data:
                affiliation_instance, _ = Affiliation.objects.get_or_create(
                    **affiliation_data
                )
                doctor_additional_connector.affiliation.add(affiliation_instance)

            for language_spoken_data in languages_spoken_data:
                language_spoken_instance, _ = LanguageSpoken.objects.get_or_create(
                    **language_spoken_data
                )
                doctor_additional_connector.language_spoken.add(
                    language_spoken_instance
                )

            return doctor_additional_connector
