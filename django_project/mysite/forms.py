from django import forms
from .models import Events, MysiteOrganizers, Customplaces


class AddNewEvent(forms.ModelForm):
    class Meta:
        model = Events
        # required = True
        fields = ('owner', 'title', 'description', 'image', 'thumb', 'location', 'start_date', 'start_time',
                  'organizer', 'tag_it', 'is_free')


class CustomPlacesForm(forms.ModelForm):
    class Meta:
        model = Customplaces
        # required = True
        # fields = ('vk_id', 'vk_type', 'name', 'logo', 'url', 'followers', 'place_id')
        exclude = ('modified', 'created', 'is_deleted')