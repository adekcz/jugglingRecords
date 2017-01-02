"""Contains database schema and classes used to
manipulate with data"""
from django.db import models

from django.contrib.auth.models import User


def urlize(string):
    return string.replace(" ", "-")

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    info_url = models.URLField()
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
    pattern = models.CharField(max_length=200)

    def __str__(self):
        return str(self.prop_count) + " " +  str(self.prop) + " " + str(self.pattern)

#todo probably needs much more systematic approach
#(either heavy validation on allowable patter names, or better __str__)
    def as_url_part(self):
        return urlize(self.__str__())

class Record(models.Model):
    """Model for entries"""
    user = models.ForeignKey(User)
    category = models.ForeignKey(RecordCategory)
    record_happened = models.DateTimeField('when record was juggled')
    url_to_proof = models.URLField()
    approved = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    catches = models.IntegerField(default=None, blank=True, null=True)
    endurance_time = models.DurationField(default=None, blank=True, null=True)
    def __str__(self):
        return str(self.user.username) + " " +  str(self.category) + " " + str(self.endurance_time)
