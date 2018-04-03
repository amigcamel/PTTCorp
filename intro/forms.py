from django import forms
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(), max_length=10)
    email = forms.EmailField()
    subject = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea())
    captcha = CaptchaField()
