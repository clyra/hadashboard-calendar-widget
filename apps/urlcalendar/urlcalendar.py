import appdaemon.plugins.hass.hassapi as hass
from requests import get
import json
from datetime import date, timedelta

import icalendar
import recurring_ical_events

class UrlCalendar(hass.Hass):

    def initialize(self):
        self.urlcalendars = []
        self.sensorname = "sensor.calendar"
        self.update = 10
        self.debug = False
        self.state = "on"

        if "debug" in self.args:
            self.debug = self.args['debug'] 

        if "sensorname" in self.args:
            self.sensorname = "sensor." + self.args['sensorname']

        if "update" in self.args:
            self.update = self.args['update']

        if "urlcalendars" in self.args:
            for urlcal in self.args['urlcalendars']:
                self.urlcalendars.append(urlcal)
                self.mylog('adding {}'.format(urlcal))
        else:
          self.log("urlcalendars is empty!")
        
        self.run_every(self.update_cal, "now", self.update * 60 )
    
    def update_cal(self, kwargs):
        self.mylog("updating")
        
        start_date = self.datetime() - timedelta(days=10)
        end_date = self.datetime() + timedelta(days=30)

        events = []
        
        for cal in self.urlcalendars:
          self.mylog(cal)

          try:
            r = get(cal, verify=False)
            current_cal = icalendar.Calendar.from_ical(r.text)
          except:
            self.log('error retrieving calendar {}'.format(cal))

          try:  
            current_events = recurring_ical_events.of(current_cal).between(start_date, end_date)
            for event in current_events:
              summary = event['SUMMARY']
              start = event["DTSTART"].dt.isoformat()
              end = event["DTEND"].dt.isoformat()
              current_event = { "title": summary, "start": start, "end": end}
              
              self.mylog("{}: {} {}".format(summary, start, end))
            
              events.append(current_event)
          except:
            self.log('error parsing calendar {}'.format(cal))

        self.mylog(events)

        json_attr = { 'json': events }

        self.set_state(self.sensorname, state=self.state, attributes=json_attr) 
          
 
    def mylog(self, s):
        if self.debug:
            self.log(s)

