from django.contrib import admin

from .models import Achievement, Degree, Department, Doctor, DoctorAdditionalConnector

admin.site.register(Achievement)
admin.site.register(Degree)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(DoctorAdditionalConnector)
