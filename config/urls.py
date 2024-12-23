from django.contrib import admin
from django.urls import path, include
from django.urls.conf import re_path
from django.conf.urls.static import static
from django.conf import settings

from core import views as core_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Acteezer API",
      default_version='v1',
      description="Acteezer APP swagger",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    path('api/account/',include('account.api.urls',namespace='account-api')),
    path('api/core/',include('core.api.urls',namespace='core-api')),
    path('api/activity/',include('activity.api.urls',namespace='activity-api')),
]