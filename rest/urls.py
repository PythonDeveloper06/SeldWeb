from django.urls import path, include, re_path
from rest_framework_extensions.routers import ExtendedSimpleRouter

from rest.views import DeviceViewSet, KeysViewSet

router = ExtendedSimpleRouter()
router.register(r'devices', DeviceViewSet, basename='DeviceViewSet') \
      .register(r'keys', KeysViewSet, basename='KeysViewSet', parents_query_lookups=['device'])

urlpatterns = [
    path('api/v1.0/', include(router.urls)),
    path('api/v1.0/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]
