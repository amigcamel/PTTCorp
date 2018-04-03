from django import forms


class SentipolForm(forms.Form):
    box = forms.CharField(widget=forms.Textarea(), label=(""))
