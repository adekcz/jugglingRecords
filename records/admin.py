""" Used to specify parameters for hidden administration """
from django.contrib import admin

from .models import Record, RecordCategory, UserProfile

USED_MODELS = [Record, UserProfile, RecordCategory]  # iterable list

admin.site.register(USED_MODELS)
