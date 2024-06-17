from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("super-admin/", admin.site.urls),
    path("admin", include("admin.api.urls")),
]
