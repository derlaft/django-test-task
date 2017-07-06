from django.conf.urls import url, include
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from activity.models import (
        SleepActivity,
        GeoActivity,
        StepActivity,
        SleepActivitySerializer,
        GeoActivitySerializer,
        StepActivitySerializer,
        )

activity_models = {
        'geo': (GeoActivity, GeoActivitySerializer),
        'sleep': (SleepActivity, SleepActivitySerializer),
        'step': (StepActivity, StepActivitySerializer),
        }

activity_types = list(
        activity_models.keys(),
        )


class ActivityRequest(serializers.Serializer):
    """ Class for a generic activity query """
    activity_type = serializers.ChoiceField(
            # get correct values from activity_types keys
            choices=activity_types,
            )


class ActivitySearch(serializers.Serializer):
    """ Search activity by date """
    search_from = serializers.DateTimeField()
    search_to = serializers.DateTimeField()


@api_view(['POST', 'PUT'])
def activity(request):

    # get request type -- and corresponding model && serializer
    req = ActivityRequest(data=request.data)
    if not req.is_valid():
        return Response(req.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    model, serializer = activity_models[req.validated_data['activity_type']]

    # create new activity
    if request.method == 'PUT':

        if 'activity' not in request.data:
            return Response("You must specify an object to create",
                            status=status.HTTP_400_BAD_REQUEST)

        # check input data
        serializer_instance = serializer(data=request.data['activity'])

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # query activity by date
    elif request.method == 'POST':

        # re-check input data
        req = ActivitySearch(data=request.data)
        if not req.is_valid():
            return Response(req.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        # query results (task requires filtering only by time_start)
        objects = model.objects.all().filter(
                time_start__gte=req.validated_data['search_from'],
                time_start__lte=req.validated_data['search_to'],
                )

        serializer_instance = serializer(objects, many=True)
        return Response(serializer_instance.data)


urlpatterns = [
        url(r'^activities/', activity),
        url(r'^api/',
            include('rest_framework.urls', namespace='rest_framework')),
        ]
