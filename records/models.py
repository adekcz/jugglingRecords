"""Contains database schema and classes used to
manipulate with data"""
from datetime import date

from django.db import models

from django.contrib.auth.models import User


def urlize(string):
    return string.replace(" ", "-")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    info_url = models.URLField(
        null=True,
        blank=True,
        )
    def __str__(self):
        return self.user.username

class RecordCategory(models.Model):
    """Model for record categories"""
    BALLS = 'BALLS'
    BBALLS = 'BBALLS'
    CLUBS = 'CLUBS'
    RINGS = 'RINGS'
    PROPS_CHOICES = (
        (BALLS, 'Balls'),
        (BBALLS, 'Bouncing Balls'),
        (CLUBS, 'Clubs'),
        (RINGS, 'Rings'),
    )
    prop = models.CharField(
        max_length=10,
        choices=PROPS_CHOICES,
        default=BALLS,
    )
    prop_count = models.IntegerField()
    pattern = models.CharField(
        max_length=200,
        blank=True,
        )

    def __str__(self):
        return str(self.prop_count) + " " +  str(self.prop) + " " + str(self.pattern)

#todo probably needs much more systematic approach
#(either heavy validation on allowable patter names, or better __str__)

class Record(models.Model):
    """Model for entries"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        verbose_name=" record",
        to=RecordCategory,
        on_delete=models.CASCADE,
        )
    record_happened = models.DateField(
        verbose_name=" date",
        default=date.today,
        )
    url_to_proof = models.URLField(" video/evidence url", null=True, blank=True)
    approved = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    catches = models.IntegerField(" catches", default=None, null=True, blank=True)
    endurance_time = models.DurationField(default=None, null=True, blank=True)
    def __str__(self):
        return str(self.user.username) + " " +  str(self.category) + " " + str(self.endurance_time)
