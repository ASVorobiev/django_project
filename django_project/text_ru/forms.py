from django import forms


class TextForm(forms.Form):
    description = forms.CharField()

