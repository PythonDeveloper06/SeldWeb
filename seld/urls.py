from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('seld/', views.home, name='seld'),
    path('about/', views.about, name='about'),
    path('download_apk_file/', views.download_file, name="download_apk_file")
]
