from django import forms
from .models import RawData, DataFolder

class DataForm(forms.ModelForm):
    class Meta:
        model = RawData
        fields = ('data', 'px_my', 'pattern_file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['px_my'].queryset = RawData.objects.using('retina').none()


        if 'data' in self.data:
            try:
                data_id = int(self.data.get('data'))
                self.fields['px_my'].queryset = RawData.objects.using('retina').filter(country_id=data_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['px_my'].queryset = self.instance.country.city_set.order_by('name')