"""
Implementation of a brush selector. This class maintains selection state
between multiple data sources by monitoring their metadata for changes.
"""
from chaco.abstract_brush_selector import AbstractBrushSelector
import numpy as np

class BrushSelector(AbstractBrushSelector):
    """
    This class implements AbstractBrushSelector as a simple data brush manager.
    Brushes can be added to the selector and data sources can be subscribed to.
    All subscribed datasources are monitored for changes to the brush mask
    metadata and changes to the mask are propagated to all subscribed 
    datasources.
    """
    
    def subscribe(self,source):
        """
        Add a new data source the list of subscribed data sources. Configure
        the correct actions to take when selections are changed.
        """
        # If this is the first data source to be added, create the mask.
        if len(self.subscribed_data) == 0:
            #Create a mask with all values set to False
            mask = np.zeros(source.get_size,bool)
            source.metadata[self.metadata_name] = mask 
            self.subscribed_data.append(source)
        else:
            if source not in self.subscribed_data:
                self.subscribed_data.append(source)
    
    def unsubscribe(self,source):
        """
        Remove a data source from the list of subscribed data sources. Remove
        any actions that were configured to handle selection changes. On the
        data source.
        """
        if source in self.subscribed_data:
            self.subscribed_data.remove(source)
    
    def _update_selection(self,changed_object, event):
        """
        Updates the brush selections. In this simple case, the new mask is just
        copied over top of the brush selections in the remaining subscribed
        data sources.
        """
        for data_source in [source for source in self.subscribed_data if source is not changed_object]:
            data_source.metadata[self.metadata_name] = changed_object.metadata[self.metadata_name]