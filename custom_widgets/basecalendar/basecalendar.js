function basecalendar(widget_id, url, skin, parameters)
{
    self = this;

    // Initialization

    self.widget_id = widget_id;

    self.parameters = parameters;

    var callbacks = [];
  
    self.OnStateAvailable = OnStateAvailable;
    self.OnStateUpdate = OnStateUpdate;

    var monitored_entities =  [];

    if ("entity" in parameters)
    {
        monitored_entities =
            [
                {"entity": parameters.entity, "initial": self.OnStateAvailable, "update": self.OnStateUpdate}
            ]
    }

    if ("entities" in parameters)
    {
        for (var e in parameters.entities){
            monitored_entities.push({"entity": e, "initial": self.OnStateAvailable, "update": self.OnStateUpdate}) 
        }
    }

    if ("view" in parameters)
    {   
        // dayGridDay, dayGridWeek, dayGridMonth, timeGridDay, timeGridWeek,
        // listDay,listWeek, listMonth
        var my_view = parameters.view;
    } else {
        var my_view = "listDay";
    }
    
    if ("fullcalendar_options" in parameters)
    {   
        var my_options = parameters.fullcalendar_options;
    } else {
        var my_options = {
              displayEventTime: true,
              height: "100%",
              initialView: my_view,
              headerToolbar: {
                start: 'prev,next,today',
                center: 'title',
                end: ''
              },
            }  
    }

    WidgetBase.call(self, widget_id, url, skin, parameters, monitored_entities, callbacks);

    var calendarEl = document.getElementById(widget_id).getElementsByClassName("inner-calendar")[0];
    var calendar = new FullCalendar.Calendar(calendarEl, my_options); 
    
    function getOptions(self, source)
    {
        if ("entities" in self.parameters)
        {
            if (source in self.parameters.entities)
            {
                return self.parameters.entities[source];
            }
        }
    }

    function OnStateAvailable(self, state)
    {
        
        if ("json" in state.attributes)
        {
            var x = { id: state.entity_id, 'events': state.attributes.json};
            var source = Object.assign({}, x, getOptions(self, state.entity_id));

            //check if the source already exist to avoid duplication
            if (calendar.getEventSourceById(state.entity_id))
            {
                calendar.getEventSourceById(state.entity_id).remove();
            }
            
            calendar.addEventSource( source );
            calendar.render();
        }
    }

    function OnStateUpdate(self, state)
    {
        if ("json" in state.attributes)
        {
            var x = { id: state.entity_id, 'events': state.attributes.json};
            var source = Object.assign({}, x, getOptions(self, state.entity_id));
            
            calendar.getEventSourceById(state.entity_id).remove();
            calendar.addEventSource( source );
        }
    }

}
