from django import forms
from .models import Events, MysiteOrganizers, Customplaces


class AddNewEvent(forms.ModelForm):
    class Meta:
        model = Events
        # required = True
        fields = ('owner', 'title', 'description', 'image', 'thumb', 'location', 'start_date', 'start_time',
                  'organizer', 'tag_it', 'is_free', 'place')


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