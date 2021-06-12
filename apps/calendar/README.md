# Calendar app

The calendar app retrieve events from a Home Assistant calendar and add then
to the "json" atribute using a format ready to be used by the calendar widget.

The app accepts the following parameters:

Variable  |  value(ex)  | obs   
----------|----------|----
sensorname| myname   | the app will create a sensor.myname to hold the events
update    | 1        | time in minutes between updates
calendars | calendar.ical_ha | the HA calendar entity to retrieve events. It could be a comma separated list
debug     |   false | enable/disable debug messages on appdaemon logs

## Configuration example

The following example will create a sensor.cal_test1 and will retrieve events 
from two calendars, updating them every 5 minutes. 
 
```yaml
CalendarTest1:
  module: calendar
  class: Calendar
  debug: True
  sensorname: cal_test1
  update: 5 
  calendars: calendar.ical_test1, calendar.ical_test2
  ```
