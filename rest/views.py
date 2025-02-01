import datetime

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from set.forms import AddKeysModel
from set.models import DeviceModel, Keys
from set.utils import timepp
from .serializers import DeviceSerializer, KeysSerializer


class DeviceViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = DeviceSerializer
    lookup_field = 'serial_num'

    def get_queryset(self):
        user = self.request.user
        return DeviceModel.objects.filter(user=user)


class KeysViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = KeysSerializer

    def get_queryset(self):
        s_num = self.kwargs['parent_lookup_device']
        device_lock = DeviceModel.objects.get(serial_num=s_num)
        keys = Keys.objects.filter(device_id=device_lock.id)
        return keys

    def list(self, request, pytz=None, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        for query in queryset:
            key_time = timezone.now()
            print(timezone.now(), query.time_end)
            if query.used == 'T':
                if key_time > query.time_end:
                    Keys.objects.get(pk=query.id).delete()

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        time_end = request.data['time_end']
        slct = request.data['selection']
        time_d = timepp(time_end, slct)

        form = AddKeysModel({
            'key': request.data['key'],
            'used': request.data['used'],
            'time_start': timezone.now(),
            'time_end': time_d,
            'selection': request.data['selection'],
            'device': request.data['device'],
        })

        if form.is_valid():
            if not Keys.objects.filter(key=request.data['key']):
                form.save()
                return Response("Key save")
            return Response("Key exist")
        return Response("Key no save")
