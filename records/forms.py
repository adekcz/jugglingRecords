"""Contains forms used in application"""
from django.contrib.auth.models import User
from django.forms import ModelForm, RadioSelect
from nocaptcha_recaptcha.fields import NoReCaptchaField

from .models import Record, UserProfile, RecordCategory


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

class UserSimpleForm(ModelForm):
    """Form for registration page"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class UserProfileForm(ModelForm):
    """Form for edit user setting form"""
    class Meta:
        model = UserProfile
        fields = ('info_url', )

class RecordsFilterForm(ModelForm):
    """Form for edit user setting form"""
    class Meta:
        model = RecordCategory
        fields = ('prop', 'record_type', )
        widgets = {'prop': RadioSelect(
            attrs={'onclick': 'this.form.submit()', 'onChange': 'this.form.submit();', "class":"rb w-radio-input"}),
                   'record_type': RadioSelect(
                       attrs={'onChange': 'this.form.submit();', "class":"rb w-radio-input"})}
