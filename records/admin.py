from django.contrib import admin

from .models import *

myModels = [Record, UserProfile, RecordCategory]  # iterable list

admin.site.register(myModels)
