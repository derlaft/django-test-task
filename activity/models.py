from django.db import models
from rest_framework import serializers

# Create your models here.


class Activity(models.Model):

    # base fields for any activity
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    class Meta:
        abstract = True


class SleepActivity(Activity):

    # sleep activities usually have some stages
    # but none are mentioned in the task description
    pass


class SleepActivitySerializer(serializers.HyperlinkedModelSerializer):
    """ Serializers define the API representation. """

    class Meta:
        model = SleepActivity
        fields = ('time_start', 'time_end')


class StepActivity(Activity):

    steps = models.IntegerField()


class StepActivitySerializer(serializers.HyperlinkedModelSerializer):
    """ Serializers define the API representation. """

    class Meta:
        model = StepActivity
        fields = ('time_start', 'time_end', 'steps')


class GeoActivity(Activity):

    latitude = models.FloatField()
    longitude = models.FloatField()


class GeoActivitySerializer(serializers.HyperlinkedModelSerializer):
    """ Serializers define the API representation. """

    class Meta:
        model = GeoActivity
        fields = ('time_start', 'time_end', 'latitude', 'longitude')
