"""
Scatter plot with panning and zooming

Shows a scatter plot of a set of random points,
with basic Chaco panning and zooming.

Interacting with the plot:

- Left-mouse-drag pans the plot.
- Mouse wheel up and down zooms the plot in and out.
- Pressing "z" brings up the Zoom Box, and you can click-drag a rectangular
region to zoom. If you use a sequence of zoom boxes, pressing alt-left-arrow
and alt-right-arrow moves you forwards and backwards through the "zoom
history".
"""

# Major library imports
from numpy import sort

import numpy as np

# Enthought library imports
from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Item, Group, View

# Chaco imports
from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import PanTool, ZoomTool
from enable.colors import color_table
import enable.colors
import random
from chaco.discrete_color_mapper import DiscreteColorMapper
from chaco.data_view import DataView
from chaco.colormapped_scatterplot import ColormappedScatterPlot
from chaco.array_data_source import ArrayDataSource
from chaco.color_data_source import ColorDataSource
from chaco.axis import PlotAxis
from chaco.data_range_1d import DataRange1D
from chaco.linear_mapper import LinearMapper
from chaco.colormapped_selection_overlay import ColormappedSelectionOverlay
from chaco.tools.lasso_selection import LassoSelection
from chaco.lasso_overlay import LassoOverlay
from traits.trait_types import Button


#===============================================================================
# # Create the Chaco plot.
#===============================================================================
def _create_plot_component():

    # Create some data
    numpts = 25
    x = sort(np.random.random(numpts))
    y = np.random.random(numpts)
    index = ArrayDataSource(x)
    value = ArrayDataSource(y)

   
    # Generate Random colors
    # The arrays must be RGBA color tuples. Create the appropriate arrays.
    colors=[]
    for i in range(len(x)):
        colors.append(random.choice(enable.colors.color_table.keys()))

    color_mapper = DiscreteColorMapper()
    index_range=DataRange1D(index)
    index_mapper=LinearMapper(range=index_range)
    value_range=DataRange1D(value)
    value_mapper=LinearMapper(range=value_range)    



    plot_view = DataView(border_visible = True,
                         padding = 25,
                         fixed_preferred_size = (100,85)
                         )
        
    plot_view.use_backbuffer = True
    plot_view.padding_left = 40
    plot_view.padding_right = 5
    plot_view.padding_top = 15
    color_data = ColorDataSource(colors)

    points=ColormappedScatterPlot(index=ArrayDataSource(x),
                        value=ArrayDataSource(y),
                        color_data = color_data,
                        index_mapper=index_mapper,
                        value_mapper=value_mapper,
                        color_mapper = color_mapper,
                        marker_size=3,
                        render_method = 'bruteforce'
                        )              
    #Need to create and add the axis. Add it to the z_line.
    left=PlotAxis(orientation='left',title='Y',
                  mapper=value_mapper,
                  component=points)
    bottom=PlotAxis(orientation='bottom',title='X',
          mapper=index_mapper,
          component=points)        
    
    points.underlays.append(left)
    points.underlays.append(bottom)
    
    plot_view.add(points)
#
#    # Tweak some of the plot properties
#    plot.title = "Scatter Plot"
#    plot.line_width = 0.5
#    plot.padding = 50
#
    # Attach some tools to the plot
    points.tools.append(PanTool(points, constrain_key="shift"))
    zoom = ZoomTool(component=points, tool_mode="box", always_on=False)
    points.overlays.append(zoom)
    
    # Attach some tools to the plot
    lasso_selection = LassoSelection(component=points,
                                     selection_datasource=color_data,
                                      metadata_name='selection_masks'
                                      )
#                        
    points.active_tool = lasso_selection
#                        scatter.tools.append(ScatterInspector(scatter))
    lasso_overlay = LassoOverlay(lasso_selection=lasso_selection,
                                 component=points)
    points.overlays.append(lasso_overlay)    
    
    selection = ColormappedSelectionOverlay(points, fade_alpha=0.35,
                                        selection_type="mask",
                                        selected_outline_width = 5)
    points.overlays.append(selection)

    return plot_view

#===============================================================================
# Attributes to use for the plot view.
size = (650, 650)
title = "Basic scatter plot"
bg_color="lightgray"

#===============================================================================
# # Demo class that is used by the demo.py application.
#===============================================================================
class Demo(HasTraits):
    plot = Instance(Component)
    
    select_button = Button(label='Select')    
    
    traits_view = View(
                    Group(
                        Item('plot', editor=ComponentEditor(size=size,
                                                            bgcolor=bg_color),
                             show_label=False),
                        orientation = "vertical"),
                        Item('select_button',
                             show_label=False),                                              
                    resizable=True, title=title
                    )
    def _select_button_fired(self,event):
        renderer = self.plot._components[0]
        data_source = renderer.color_data
        data_source.metadata['selection_masks'] = np.ones(25)
        print "select button" 
    def _plot_default(self):
        return _create_plot_component()

demo = Demo()

if __name__ == "__main__":
    demo.configure_traits()

#--EOF---