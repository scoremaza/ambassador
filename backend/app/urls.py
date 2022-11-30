from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Ambassador API",
        default_version="v1",
        description="API endpoints for the Ambassador API",
        contact=openapi.Contact(email="info@enlighten-e.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/admin/", include("administrator.urls")),
    path("api/v1/ambassador/", include("ambassador.urls")),
    path("api/v1/checkout/", include("checkout.urls")),
    path("api/v1/profile", include("profiles.urls")),
]

admin.site.site_header = "Ambassador API Admin"
admin.site.site_title = "Ambassador API Admin Portal"
admin.site.index_title = "Welcome to the Ambassador API Portal"
