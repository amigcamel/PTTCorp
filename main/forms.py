#-*-coding:utf-8-*-
from django import forms

from registration.forms import RegistrationFormTermsOfService
from captcha.fields import CaptchaField

from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationForm

from passwords.fields import PasswordField

import re


from django.contrib.auth.models import User


def ajiEmailValidator(email):
    allow_list = ['@gmail\.', '@hotmail\.', '@yahoo\.', '@.*?\.edu']
    pat = re.compile('|'.join(allow_list))
    if not pat.search(email):
        raise forms.ValidationError(u'Sorry, you can\'t use this email!')
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError(u'This email has been used!')


class RegForm(RegistrationForm):
    # modified from here:
    # /usr/local/lib/python2.7/dist-packages/registration/forms.py
    username = forms.RegexField(
        regex=r'^[a-zA-Z0-9]+$',
        min_length=5,
        max_length=30,
        label=("Username"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}),
        error_messages={
            'invalid': ("Username may contain only letters and numbers")},
        help_text="Username may contain at least 5 alphanumeric characters with only letters and numbers ")

    email = forms.EmailField(
        validators=[ajiEmailValidator],
        label=("E-mail"),
        help_text='Currently you can only register with gmail, hotmail, yahoo or .edu domain (i.e. @ntu.edu.tw).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'email'}),
    )
#    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),
#                                label=("Password"))
    password1 = PasswordField(
        label="Password",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'password'}),
        help_text="Password may contains at least 5 characters with not too simple sequence (i.e. 12345, qwerty).")
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'type': 'password'}),
        label=("Password (again)"))


#    tos = forms.BooleanField(widget=forms.CheckboxInput,
#                             label=(u'I have read and agree to the Terms of Service'),
# error_messages={'required': ("You must agree to the terms to
# register")})
    captcha = CaptchaField()
