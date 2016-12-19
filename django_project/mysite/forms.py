from django import forms
from django.forms import ModelChoiceField

from .models import Events, MysiteOrganizers, Customplaces, Locations


class AddNewEvent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewEvent, self).__init__(*args, **kwargs)
        self.fields['location'].required = True
        self.fields['location'].queryset = self.fields['location'].queryset.exclude(created=0, is_deleted=1).order_by('name')
        self.fields['place'].required = True
        self.fields['start_date'].required = True
        self.fields['start_time'].required = True

    class Meta:
        model = Events
        fields = ('owner', 'title', 'description', 'image', 'thumb', 'location', 'start_date', 'start_time',
                  'organizer', 'tag_it', 'is_free', 'place', 'export_vk', 'is_active', 'url')


class ConfidenceNewEvent(forms.ModelForm):
    class Meta:
        model = Events
        # required = True
        fields = ('owner', 'title', 'description', 'image', 'thumb', 'location', 'start_date', 'start_time',
                  'finish_date', 'duration',
                  'organizer', 'tag_it', 'is_free', 'place', 'url', 'is_active', 'export_vk')

class CustomPlacesForm(forms.ModelForm):
    class Meta:
        model = Customplaces
        # required = True
        fields = ('name', 'logo', 'url')
        # exclude = ('modified', 'created', 'is_deleted', 'org_parent', 'location', 'latitude', 'longitude')