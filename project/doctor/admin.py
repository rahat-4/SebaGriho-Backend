from django.contrib import admin

from .models import (
    Achievement,
    Affiliation,
    Degree,
    Department,
    Doctor,
    DoctorContact,
    LanguageSpoken,
    Schedule,
    Specialty,
)

admin.site.register(Achievement)
admin.site.register(Degree)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(DoctorContact)
admin.site.register(LanguageSpoken)
admin.site.register(Schedule)
admin.site.register(Specialty)
admin.site.register(Affiliation)
