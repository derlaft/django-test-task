import random
import datetime

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from activity.views import activity, activity_types, activity_models
from activity.models import SleepActivity, StepActivity, GeoActivity

# Create your tests here.


class ActivityTestCase(TestCase):

    CREATE_OBJECTS = 255
    START_DATE = datetime.datetime(2016, 5, 12, 12, 00, 3,
                                   tzinfo=datetime.timezone.utc)

    def setUp(self):
        self.factory = APIRequestFactory()

        self.objs = {
                'sleep': [],
                'geo': [],
                'step': [],
                }

        # create sleep objects
        for i in range(ActivityTestCase.CREATE_OBJECTS):

            start, stop = self.random_interval(ActivityTestCase.START_DATE)
            self.objs['sleep'].append(SleepActivity.objects.create(
                time_start=start,
                time_end=stop,
                ))

        # create geo objects
        for i in range(ActivityTestCase.CREATE_OBJECTS):

            start, stop = self.random_interval(ActivityTestCase.START_DATE)
            self.objs['geo'].append(GeoActivity.objects.create(
                time_start=start,
                time_end=stop,
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-90, 90),
                ))

        # create step objects
        for i in range(ActivityTestCase.CREATE_OBJECTS):

            start, stop = self.random_interval(ActivityTestCase.START_DATE)
            self.objs['step'].append(StepActivity.objects.create(
                    time_start=start,
                    time_end=stop,
                    steps=random.randint(0, 12309),
                    ))

    def random_type(self):
        """ Return a random and correct activity type """
        return random.choice(activity_types)

    def random_interval(self, date_from):
        """ Return a random interval that starts between
            date_from and date_from + 1 year and
            lasts at least for 1 day

            I guess, in real world, the intervals
            have to be measured in seconds, not days.
            Anyway, this should be fine for an example.
        """

        start = date_from + datetime.timedelta(random.randint(1, 365))
        stop = start + datetime.timedelta(random.randint(1, 10))

        return start, stop

    def test_incorrect_activity_type(self):
        req = self.factory.post('/activities/', {'activity_type': 'unknown'})
        resp = activity(req)
        assert resp.status_code != 200

    def test_missing_date_in_activity_search(self):
        req = self.factory.post('/activities/', {
            'activity_type': self.random_type(),
            })
        resp = activity(req)
        assert resp.status_code != 200

    def test_put_with_empty_activity(self):
        req = self.factory.put('/activities/', {
            'activity_type': self.random_type(),
            })
        resp = activity(req)
        assert resp.status_code != 200

    def test_select_with_invalid_date(self):
        req = self.factory.post('/activities/', {
            'activity_type': self.random_type(),
            'search_from': 'meow',
            'search_to': ActivityTestCase.START_DATE,
            })
        resp = activity(req)
        assert resp.status_code != 200

    def test_put_geo_activity(self):

        start, stop = self.random_interval(
                # insert in interval that does not cross with pre-inserted data
                ActivityTestCase.START_DATE + datetime.timedelta(days=365*2))

        latitude, longitude = random.uniform(-90, 90), random.uniform(-90, 90)

        req = self.factory.put('/activities/', dict(
            activity_type='geo',
            activity=dict(
                time_start=start,
                time_end=stop,
                latitude=latitude,
                longitude=longitude,
            ),
            ), format='json')

        resp = activity(req)
        assert resp.status_code == 200

        # not we want to check if this was inserted, query it
        req = self.factory.post('/activities/',
                                {
                                    'activity_type': 'geo',
                                    'search_from': str(start),
                                    'search_to': str(stop),
                                })
        resp = activity(req)

        assert len(resp.data) == 1
        assert resp.data[0]['longitude'] == longitude
        assert resp.data[0]['latitude'] == latitude

    def test_select_activities(self):

        for obj_type in activity_types:

            # get serializer for this obj type
            serializer = activity_models[obj_type][1]

            start, stop = self.random_interval(ActivityTestCase.START_DATE)
            req = self.factory.post('/activities/',
                                    {
                                        'activity_type': obj_type,
                                        'search_from': str(start),
                                        'search_to': str(stop),
                                    })
            resp = activity(req)
            assert resp.status_code == 200

            # select objects that are excepted to be queried
            wanted_activities = [act for act in self.objs[obj_type] if
                                 start <= act.time_start <= stop]
            serializer_instance = serializer(wanted_activities, many=True)

            assert len(resp.data) == len(serializer_instance.data)
