from django.utils import timezone

from django import forms

from .models import DeviceModel, Keys
from .utils import new_code


# !---- Device form -----!
class AddDeviceModel(forms.ModelForm):
    class Meta:
        model = DeviceModel
        fields = '__all__'

        widgets = {
            'device_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Device name',
                'name': 'device_name'
            }),
            'status': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Status'
            }),
        }


# !----- Key form -----!
class AddKeysModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_end'].initial = timezone.now()
        self.fields['key'].initial = new_code()

    key = forms.CharField(min_length=4, max_length=16,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Key'}))
    time_end = forms.DateTimeField(required=False,
                                   widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Time'}))

    class Meta:
        model = Keys
        fields = '__all__'

        widgets = {
            'used': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Used'
            }),
            'selection': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Quick selection'
            })
        }