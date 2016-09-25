from django import forms
from .models import Events


class AddNewEvent(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('title', 'description', 'image', 'thumb', 'location', 'start_date', 'start_time')

