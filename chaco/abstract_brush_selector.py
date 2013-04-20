"""
Defines an abstract brush selection manager
"""
from traits.has_traits import HasTraits, on_trait_change
from traits.trait_types import List, Str, Enum
from chaco.abstract_data_source import AbstractDataSource

class AbstractBrushSelector(HasTraits):
    """
    An abstract class for brush selectors which maintain syncronzation of
    selections between datasources. 
    """
    
    # A list of data sources to monitor for selection changes.
    subscribed_data = List(AbstractDataSource)
    
    # The name of the metadata used to hold the selection mask.
    metadata_name = Str('brush_mask')
    
    # To prevent recursion during an update, ignore incoming change events.
    selector_state = Enum('listening','updating')
    
    def subscribe(self,source):
        """
        Add a new data source the list of subscribed data sources. Configure
        the correct actions to take when selections are changed.
        """
        raise NotImplementedError()
    
    def unsubscribe(self,source):
        """
        Remove a data source from the list of subscribed data sources. Remove
        any actions that were configured to handle selection changes. On the
        data source.
        """
        raise NotImplementedError()
    
    @on_trait_change('subscribed_data:metadata')
    def handle_brush_change(self,changed_object, name, old, new):
        """
        Catches a change in the metadata dictionary to see if brush masks need
        updating. Any modification to the metadata dictionary or its items
         of a subscribed data source will result in this handler being called.
         new will contain a TraitDictEvent(althought it's not clear why)
        """
        # For clarity. New contains a TraitDictEvent
        event = new
        if self.selector_state == 'listening':
            if  self.metadata_name in (set(event.added) | set(event.removed) | set(event.changed)):
                self.selector_state = 'updating'
                self._update_selection(changed_object, event)
                self.selector_state = 'listening'
            else:
                pass
        else:
            pass
        
    def _update_selection(self,changed_object, event):
        """
        Updates the brush selections.
        """
        raise NotImplementedError()
        