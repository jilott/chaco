""" Defines the ColorMapper and ColorMapTemplate classes.
"""

# Major library imports
from types import IntType, FloatType
from numpy import arange, array, asarray, clip, divide, float32, int8, isinf, \
        isnan, ones, searchsorted, sometrue, sort, take, uint8, where, zeros, \
        linspace, ones_like,float64

# Enthought library imports
from traits.api import Any, Array, Bool, Dict, Event, Float, HasTraits, \
                                 Int, Property, Str, Trait

# Relative imports
from abstract_colormap import AbstractColormap
from data_range_1d import DataRange1D

from speedups import map_colors
from chaco.color_mapper import ColorMapper

class DiscreteColorMapper(ColorMapper):
    """ Performs discrete mapping of colors.
    
    A simple pass through for RGBA data. The actual mapping of data takes place
    in the data source.
    """

    # The color table.
    color_bands = Property(Array)

    # The total number of color steps in the map.
    steps = Int(256)

    # The name of this color map.
    name = Str

    # Not used.
    low_pos = None
    # Not used.
    high_pos = None

    # A generic "update" event that generally means that anything that relies
    # on this mapper for visual output should do a redraw or repaint.
    updated = Event

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, **kwtraits):
        """ Creates a DiscreteColorMap. It is really just a pass through.
        
        The color datasource takes care of performing the actually mapping of
        color names to RGBA data. This mapper is just a pass through to allow
        use of this type of data without making changes to any existing code.
        """
        super(AbstractColormap, self).__init__(**kwtraits)
        return


    def map_screen(self, data_array):
        """ Maps an array of data values to an array of colors.
        
        This is really just a pass through. The code simply unpacks the color
        values stored as uint32 data into RGBA tuples.
        """
        
        rgba = zeros((len(data_array),4),dtype=(float32))
        for idx,val in enumerate(data_array):
            color = zeros((4),dtype = float32)
            val = int(val)
            # Apply some shifts and masks to unpack the color values. 
            color[0] = float(val >> 24 & 0xff)/255
            color[1] = float(val >> 16 & 0xff)/255
            color[2] = float(val >> 8 & 0xff)/255
            color[3] = float(val & 0xff)/255
            rgba[idx] = color
            
        
        return rgba


    def map_index(self, ary):
        """ Maps an array of values to their corresponding color band index.
        
        Not sensible for the discrete map.
        """
        raise NotImplementedError
#        if self._dirty:
#            self._recalculate()
#
#        indices = (ary - self.range.low) / (self.range.high - self.range.low) * self.steps
#
#        return clip(indices.astype(IntType), 0, self.steps - 1)

    def reverse_colormap(self):
        """ Reverses the color bands of this colormap.
        
        Not sensible for the discrete map.
        """
        raise NotImplementedError
#        for name in ("red", "green", "blue", "alpha"):
#            data = asarray(self._segmentdata[name])
#            data[:, (1,2)] = data[:, (2,1)]
#            data[:,0] = (1.0 - data[:,0])
#            self._segmentdata[name] = data[::-1]
#        self._recalculate()


    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------


    def _range_changed(self, old, new):
        if old is not None:
            old.on_trait_change(self._range_change_handler, "updated",
                                remove = True)
        if new is not None:
            new.on_trait_change(self._range_change_handler, "updated")

        self.updated = new

    def _range_change_handler(self, obj, name, new):
        "Handles the range changing; dynamically attached to our ranges"
        self.updated = obj



# EOF
