from rest_framework.generics import ListCreateAPIView

from doctor.models import DoctorAdditionalConnector

from ..serializers.doctors import AdminDoctorListSerializer


class AdminDoctorList(ListCreateAPIView):
    queryset = DoctorAdditionalConnector.objects.all()
    serializer_class = AdminDoctorListSerializer
