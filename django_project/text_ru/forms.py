from django import forms


class TextForm(forms.Form):
    message = forms.CharField()

