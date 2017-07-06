# django-test-task

This is sample django test task

## API calls

* Create an activity:

```
PUT /activities

{
   "activity_type": "step",
   "activity": {
       "time_start": "2012-12-12T12:12+0300",
       "time_stop": "2012-12-12T12:42+0300",
       "steps": 42
   }
}

PUT /activities

{
   "activity_type": "sleep",
   "activity": {
      "time_start": "2012-12-12T12:12+0300",
      "time_stop": "2012-12-12T12:42+0300"
   }
}

PUT /activities

{
   "activity_type": "geo",
   "activity": {
      "time_start": "2012-12-12T12:12+0300",
      "time_stop": "2012-12-12T12:42+0300",
      "latitude": 50.42,
      "longitude": 54.19
   }
}
```

* Search for an activity

```
POST /activities

{
   "activity_type": "geo",
   "search_from": "2012-12-12T12:12+0300",
   "search_to": "2012-12-12T12:42+0300"
}
```
