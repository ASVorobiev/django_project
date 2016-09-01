from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


from django import forms
from .models import Events


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('title', 'description')

class AddNewEvent(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('title', 'description', 'image', 'location', 'start_date', 'start_time')