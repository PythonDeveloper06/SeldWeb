from django.urls import path

from . import views

urlpatterns = [
    path('devices/', views.DevicesListView.as_view(extra_context={'title': 'Your devices'}), name="devices"),
    path('device/<int:pk>/keys/', views.KeysListView.as_view(extra_context={'title': 'Your keys'}), name='keys'),
    path('change_device_name/<int:pk>/', views.change_device_name, name='change_device_name'),
    path('change_status/<int:pk>/', views.change_status, name='change_status'),
    path('change_admin/<int:pk>/', views.change_admin, name='change_admin'),
    path('<int:pk>/delete_key/<int:id>/', views.delete_key, name='delete_key'),

]
