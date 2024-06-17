from django.contrib.auth import get_user_model

from rest_framework import serializers

from doctor.models import (
    Achievement,
    Affiliation,
    Degree,
    Department,
    Specialty,
    LanguageSpoken,
)

User = get_user_model()


class UserSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]


class LanguageSpokenSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageSpoken
        fields = ["language"]


class DepartmentSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["name", "description"]


class SpecialtySlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["name", "department"]


class AchievementSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["name", "source", "year"]


class DegreeSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ["name", "institute", "result", "passing_year"]


class AffiliationSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ["title", "hospital_name", "status"]
