from django.urls import include, path


urlpatterns = [
    path("", include("admin.api.urls.doctors")),
]
