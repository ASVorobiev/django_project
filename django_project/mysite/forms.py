from django import forms
from .models import Events, MysiteOrganizers


class AddNewEvent(forms.ModelForm):
    class Meta:
        model = Events
        # required = True
        fields = ('owner', 'title', 'description', 'image', 'thumb', 'location', 'start_date', 'start_time',
                  'organizer', 'tag_it', 'is_free')


class AddNewOrganizer(forms.ModelForm):
    class Meta:
        model = MysiteOrganizers
        # required = True
        fields = ('vk_id', 'vk_type', 'name', 'logo', 'url', 'followers', 'place_id')