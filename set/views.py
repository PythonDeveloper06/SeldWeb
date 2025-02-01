from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .forms import AddDeviceModel, AddKeysModel
from .models import DeviceModel, Keys
from .utils import timepp


# !----- devices -----!
class DevicesListView(LoginRequiredMixin, ListView, FormMixin):
    form_class = AddDeviceModel
    model = DeviceModel
    template_name = 'set/devices.html'
    context_object_name = 'data'
    paginate_by = 6

    def get_queryset(self):
        return DeviceModel.objects.filter(user=self.request.user)


# !----- keys -----!
class KeysListView(LoginRequiredMixin, ListView, FormMixin):
    model = DeviceModel
    template_name = 'set/keys.html'
    context_object_name = 'data'
    paginate_by = 6
    form_class = AddKeysModel
    extra_context = {'title': 'Your keys'}

    def get_queryset(self):
        return Keys.objects.filter(device_id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        device_lock = DeviceModel.objects.get(id=self.kwargs['pk'])

        time_end = request.POST['time_end']
        slct = request.POST['selection']
        time_d = timepp(time_end, slct)

        form = AddKeysModel({
            'key': request.POST['key'],
            'used': request.POST['used'],
            'time_start': request.POST.get('time_start', timezone.now()),
            'time_end': time_d,
            'selection': request.POST['selection'],
            'device': device_lock
        })

        if form.is_valid():
            if not Keys.objects.filter(key=request.POST['key']):
                form.save()
            return HttpResponseRedirect(reverse_lazy('keys', args=[self.kwargs["pk"]]))
        return HttpResponseRedirect(reverse_lazy('devices'))


# !----- htmx devices -----!
def change_device_name(request, pk):
    device = DeviceModel.objects.get(pk=pk)

    device.device_name = request.POST.get('device_name') if request.POST.get('device_name') else device.device_name
    device.save()

    return HttpResponse(device.device_name)


def change_status(request, pk):
    device = DeviceModel.objects.get(pk=pk)

    if device.status == 'Close':
        device.status = 'Open'
    else:
        device.status = 'Close'
    device.save()

    return HttpResponse(device.status)


def change_admin(request, pk):
    device = DeviceModel.objects.get(pk=pk)

    if device.admin == 'Off':
        device.admin = 'On'
    else:
        device.admin = 'Off'
    device.save()

    return HttpResponse(device.admin)


def delete_key(request, id, pk):
    Keys.objects.get(pk=id).delete()
    return HttpResponse('<p class="mb-0">Ключ удалён</p>')
