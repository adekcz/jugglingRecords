"""Contains forms used in application"""
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import Record


class RegisterForm(ModelForm):
    """Form for registration page"""
    captcha = NoReCaptchaField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class NewRecordForm(ModelForm):
    """Form for newRecord"""
    class Meta:
        model = Record
        fields = ('public', 'category', 'catches',
                  'endurance_time', 'record_happened', 'url_to_proof')

class ProfileForm(forms.Form):
    """Form for edit user setting form"""
    first_name = forms.CharField(label='Your name', max_length=100)
    last_name = forms.CharField(label='Your last name', max_length=100)
