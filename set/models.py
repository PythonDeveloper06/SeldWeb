from django.db import models
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django_userforeignkey.models.fields import UserForeignKey


class DeviceModel(models.Model):
    device_name = models.CharField(max_length=255)
    serial_num = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, default="Close")
    settings = models.CharField(max_length=255, default='-')
    admin = models.CharField(max_length=10, default='Off')
    sync = models.CharField(max_length=5, default='False')
    user = UserForeignKey(auto_user_add=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse_lazy('devices')

    def get_queryset(self):
        user = self.request.user
        queryset = self.model.objects.filter(user=user)
        return queryset


class Keys(models.Model):
    USED_CHOICES = [
        ('C', 'Constant'),
        ('T', 'Temporary'),
        ('O', 'One use')
    ]

    SELECT_CHOICES = [
        ('-', '0'),
        ('+1h', '1 hour'),
        ('+1d', '1 day'),
        ('+1w', '1 week'),
        ('+2w', '2 week'),
    ]

    key = models.IntegerField()
    used = models.CharField(max_length=10, choices=USED_CHOICES, default='T')
    time_start = models.DateTimeField(null=True)
    time_end = models.DateTimeField(null=True)
    selection = models.CharField(max_length=100, choices=SELECT_CHOICES, default='-')
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)

    def get_local_start_time(self):
        return localtime(self.time_end)

    objects = models.Manager()
