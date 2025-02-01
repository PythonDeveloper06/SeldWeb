from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import status


# Create your views here.

# !----- basic functions -----!
def home(request) -> HttpResponse:
    return render(request, 'seld/index.html', {'title': 'Home Page'})


def about(request) -> HttpResponse:
    return render(request, 'seld/about.html', {'title': 'About'})


# !----- download file apk -----!
def download_file(request):
    fl_path = 'seld/static/app/mobile_app/app-debug.apk'
    filename = 'seld.apk'

    fl = open(fl_path, 'rb')
    response = HttpResponse(fl, content_type='application/force-download')
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response


# !----- own errors -----!
def handler_403(request, exception=None) -> HttpResponse:
    return render(request, "errors/403.html", {'title': '403 - в доступе отказано!'},
                  status=status.HTTP_403_FORBIDDEN)


def handler_404(request, exception=None) -> HttpResponse:
    return render(request, "errors/404.html", {'title': '404 - страница не найдена!'},
                  status=status.HTTP_404_NOT_FOUND)


def handler_500(request, exception=None) -> HttpResponse:
    return render(request, "errors/500.html", {'title': '500 - ошибка сервера!'},
                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
