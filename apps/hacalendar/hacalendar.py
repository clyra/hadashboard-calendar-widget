import appdaemon.plugins.hass.hassapi as hass
from requests import get
import json
from datetime import date, timedelta

class HaCalendar(hass.Hass):

    def initialize(self):
        self.calendars = []
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

        if "calendars" in self.args:
            for cal in self.split_device_list(self.args['calendars']):
                self.calendars.append(cal)
        else:
          self.log("calendars is empty!")
        
        self.run_every(self.update_cal, "now", self.update * 60 )
    
    def update_cal(self, kwargs):
        self.mylog("updating")
        ha_url = self.config["plugins"]["HASS"]["ha_url"]
        token = self.config["plugins"]["HASS"]["token"]
  
        start_date = (self.datetime() - timedelta(days=10)).strftime("%Y-%m-%dT00:00:00")
        end_date = (self.datetime() + timedelta(days=30)).strftime("%Y-%m-%dT00:00:00")

        headers = {'Authorization': "Bearer {}".format(token)}

        events = []
        
        for cal in self.calendars:
          apiurl = "{}/api/calendars/{}?start={}Z&end={}Z".format(ha_url,cal,start_date,end_date)
          self.mylog(apiurl)

          try:
            r = get(apiurl, headers=headers, verify=False)
            list = json.loads(r.text)
            self.mylog(list)
          
            for element in list:
              #self.log(element)
              event = { "title": "", "start": "", "end": ""}
              if "summary" in element:
                event['title'] = element["summary"]
              if "start" in element:
                event['start'] = element["start"]
              if "end" in element:
                event['end'] = element["end"]

              self.mylog("{}: {} {}".format(event['title'], event['start'], event['end']))
            
              events.append(event)
          except:
            self.log('error retrieving calendar {}'.format(cal))

        json_attr = { 'json': events }

        self.set_state(self.sensorname, state=self.state, attributes=json_attr) 
          
 
    def mylog(self, s):
        if self.debug:
            self.log(s)

