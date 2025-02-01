from django.contrib import admin

from .models import DeviceModel, Keys

admin.site.register(DeviceModel)
admin.site.register(Keys)
