from django import forms
from .models import Events


class AddNewEvent(forms.ModelForm):
    class Meta:
        model = Events
        # required = True
        fields = ('owner', 'title', 'description', 'image', 'thumb', 'location', 'start_date', 'start_time',
                  'organizer', 'tag_it')

