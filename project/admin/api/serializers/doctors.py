from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from doctor.models import (
    Achievement,
    Affiliation,
    Degree,
    Department,
    Doctor,
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
    UserSlimSerializer,
)

User = get_user_model()


class AdminDoctorListSerializer(serializers.ModelSerializer):
    user = UserSlimSerializer()
    degrees = DegreeSlimSerializer(many=True)
    achievements = AchievementSlimSerializer(many=True)
    specialties = SpecialtySlimSerializer(many=True)
    affiliations = AffiliationSlimSerializer(many=True)
    languages_spoken = LanguageSpokenSlimSerializer(many=True)

    class Meta:
        model = Doctor
        fields = [
            "user",
            "registration_number",
            "about",
            "experience",
            "appointment_fee",
            "consultation_fee",
            "follow_up_fee",
            "check_up_fee",
            "status",
            "degrees",
            "achievements",
            "specialties",
            "affiliations",
            "languages_spoken",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            degrees_data = validated_data.pop("degrees", [])
            achievements_data = validated_data.pop("achievements", [])
            specialties_data = validated_data.pop("specialties", [])
            affiliations_data = validated_data.pop("affiliations", [])
            languages_spoken_data = validated_data.pop("languages_spoken", [])

            user_data = validated_data.pop("user")
            user = User.objects.create(**user_data)

            doctor_instance = Doctor.objects.create(user=user, **validated_data)

            for degree_data in degrees_data:
                degree_instance, _ = Degree.objects.get_or_create(**degree_data)
                doctor_instance.degrees.add(degree_instance)

            for achievement_data in achievements_data:
                achievement_instance, _ = Achievement.objects.get_or_create(
                    **achievement_data
                )
                doctor_instance.achievements.add(achievement_instance)

            for specialty_data in specialties_data:
                department_data = specialty_data.pop("department")
                department_instance, _ = Department.objects.get_or_create(
                    **department_data
                )
                specialty_instance, _ = Specialty.objects.get_or_create(
                    department=department_instance, **specialty_data
                )
                doctor_instance.specialties.add(specialty_instance)

            for affiliation_data in affiliations_data:
                affiliation_instance, _ = Affiliation.objects.get_or_create(
                    **affiliation_data
                )
                doctor_instance.affiliations.add(affiliation_instance)

            for language_spoken_data in languages_spoken_data:
                language_spoken_instance, _ = LanguageSpoken.objects.get_or_create(
                    **language_spoken_data
                )
                doctor_instance.languages_spoken.add(language_spoken_instance)

            return doctor_instance
