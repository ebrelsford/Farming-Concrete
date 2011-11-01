import itertools
from StringIO import StringIO

import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


# See http://matplotlib.sourceforge.net/users/customizing.html
font_params = {
    'sans-serif': [
        'Helvetica Neue', 'Arial', 'Liberation Sans',
        'FreeSans', 'sans-serif'],
    'size': 13.0, }
matplotlib.rc('font', **font_params)

colors_default = itertools.cycle([
    '#F2E3C4',
    #'#DE2D26',  # Medium red
    #'#2CA25F',  # Medium green
])

linestyles_default = itertools.cycle([
    '-',   # solid
    '--',  # dashed
    '-.',  # dash-dot
    ':',   # dotted
])

def _create_barchart_figure(data_dct, labels_dct, template,
                           show_title=False, set_y_origin_zero=True,
                           x_zero_indexed=False, xlabels=[]):
    """
    Given 1+ sequences, create and return a Matplotlib Figure(Canvas)
    barchart visualization.

    This function parallels _create_timeseries_figure and was derived
    from it.  While it may be possible to merge them into a single
    more general function, for now there are enough differences to
    keep them separate.
    """
    # CONTENT of figure:
    assert isinstance(data_dct, dict), \
           "Unknown type for data_dct: %s" % data_dct
    series_data = data_dct['data']
    assert all([len(this_data) > 0 for this_data in series_data])
    #series_names = data_dct.get('names')
    if 'colors' in data_dct:
        colors = itertools.cycle(data_dct['colors'])
    else:
        colors = colors_default
    # With data unpacked, start building matplotlib Figure:
    the_figure = Figure((6,6))
    the_figure.subplots_adjust(left=0.08, bottom=0.2)
    ax = the_figure.add_subplot(1, 1, 1)
    plotted_data = []
    bar_width = 0.7
    for series in series_data:
        x_indices = np.arange(1, len(series) + 1)
        if x_zero_indexed:
            x_indices = np.arange(len(series))
        # Note that ax.bar() returns a single list - different from
        # ax.plot() in timeseries chart.
        this_series = ax.bar(
            x_indices,
            series,
            bar_width,
            color=colors.next(),
            edgecolor='#AAAAAA',  # Softens appearance considerably.
            #align='center',  # Causes bad spacing on chart's left.
            )
        plotted_data.append(this_series)
    ax.set_xticks(x_indices + (bar_width / 2))
    ax.set_xticklabels(xlabels or x_indices, rotation=45, horizontalalignment='right')
    ax.autoscale()
    ax.margins(.05, 0)
    # Set the legend?  Defer for now.
    #
    # Set labels: x, y
    if 'x' in labels_dct:
        ax.set_xlabel(labels_dct['x'])
    else:
        ax.set_xlabel('')
    # Note: for y-axis labels, will incorporate formatter as shown
    # here:
    # http://matplotlib.sourceforge.net/examples/pylab_examples/custom_ticker1.html
    if 'y' in labels_dct:
        ax.set_ylabel(labels_dct['y'])
    else:
        ax.set_ylabel('Data')
    # With content of the figure settled, stylize it with mutator
    # function:
    _stylize_figure(the_figure)
    return FigureCanvas(the_figure)

def create_chart_as_png_str(chart_type, data_dct,
                            labels_dct=None, template=None, xlabels=None):
    """
    This is the public-facing API call to create and return a chart as
    a PNG-format string.
    """
    assert chart_type in ('timeseries', 'barchart')
    assert isinstance(data_dct, dict) and 'data' in data_dct
    assert len(data_dct['data'][0]) > 0  # At least one sequence given.
    if labels_dct:
        assert isinstance(labels_dct, dict)
        assert 'title' in labels_dct
    # With arguments checked, create the matplotlib Figure instance
    # per chart_type:
    if chart_type == 'barchart':
        figure_fn = _create_barchart_figure
    else:
        raise Exception("Unknown chart_type %s" % chart_type)
    figure = figure_fn(data_dct, labels_dct, template, xlabels=xlabels)
    # From here on, PNG-specific code happens.
    #
    # Note: there's no need to specify resolution/DPI for web-usage,
    # what matters is the pixel count.  See
    # http://benthinkin.net/imagery/on-the-web-dpi-doesn-t-matter
    img_data_str = StringIO()
    figure.print_png(img_data_str)
    img_data_str.seek(0)  # After writing, rewind data for further use.
    return img_data_str.read()

def _stylize_figure(the_figure, style_template=None):
    """
    A mutator that updates the appearance of the given Figure
    instance, per style_template.  There is no return value.

    This code was originally part of _create_timeseries_figure, but is
    much better being separate.
    """
    # Later, the template parameter will set the overall styling of
    # the chart, including these parameters below:
    bgcolor = '#FFFFFF'
    border_color = '#CCCCCC'
    axis_label_color = '#000000'
    axis_ticks_color = '#555555'
    # Change the overall background color, which is grey by default:
    the_figure.patch.set_color(bgcolor)
    for ax in the_figure.get_axes():
        # Changing the border of a matplotlib chart is clumsy, but here it
        # is per http://stackoverflow.com/q/1982770/294239
        for child in ax.get_children():
            if isinstance(child, matplotlib.spines.Spine):
                child.set_color(border_color)
        # Next, change the color of the title, and axis+tick labels:
        #
        # This does not work to select the figure title:
        # the_figure.gca().axes.title.set_color(axis_label_color)
        #
        #if figure_title:
        #    figure_title.set_color(axis_label_color)
        ax.xaxis.get_label().set_color(axis_label_color)
        for label in ax.xaxis.get_ticklabels():
            label.set_color(axis_ticks_color)
        ax.yaxis.get_label().set_color(axis_label_color)
        for label in ax.yaxis.get_ticklabels():
            label.set_color(axis_ticks_color)
    return
