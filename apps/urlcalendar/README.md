# URLCalendar app

The URLCalendar app retrieve events from a online 'ics' calendar and add then
to the "json" atribute of a sensor using a format ready to be used by the 
calendar widget.

The app accepts the following parameters:

Variable  |  value(ex)  | obs   
----------|----------|----
sensorname| myname   | the app will create a sensor.myname to hold the events
update    | 1        | time in minutes between updates
urlcalendars | - https://www.calendarlabs.com/ical-calendar/ics/226/UN_Holidays.ics | A list with urls to retrieve ics files
debug     |   false | enable/disable debug messages on appdaemon logs

## Configuration example

The following example will create a sensor.cal_test1 and will retrieve events 
from two calendars, updating them every 5 minutes. 
 
```yaml
CalendarTest1:
  module: hacalendar
  class: HaCalendar
  debug: True
  sensorname: cal_test1
  update: 5 
  urlcalendars: 
    - https://www.calendarlabs.com/ical-calendar/ics/76/US_Holidays.ics
    - https://www.calendarlabs.com/ical-calendar/ics/226/UN_Holidays.ics
  ```
