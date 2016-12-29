from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Record

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class NewRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ('public','category', 'catches', 'endurance_time', 'record_happened', 'url_to_proof' )
