from datetime import datetime
import os

from django.conf import settings

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import pylab


def make_chart_name(metric_name, garden):
    return '_'.join([
        datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'),
        str(garden.pk),
        metric_name,
    ])


def _format_ticks(axis):
    # Remove top, right ticks
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)

    # Remove top, right ticks
    axis.xaxis.set_ticks_position('bottom')
    axis.yaxis.set_ticks_position('left')

    # Make ticks face out
    axis.xaxis.set_tick_params(direction='out')
    axis.yaxis.set_tick_params(direction='out', labelsize=14)


def _save_chart(destination_file, shape='square', **kwargs):
    # Do our best to get an appropriate file name and make room for it
    img_file = destination_file
    if not img_file.endswith('.png'):
        img_file = '%s.png' % img_file
    filename = os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'charts', img_file))
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    if shape == 'short':
        plt.gcf().set_size_inches(10, 5)

    # Save
    pylab.savefig(filename, bbox_inches='tight')

    # Close this plot so we don't affect other plots
    plt.clf()
    plt.cla()
    plt.close()
    return os.path.join('charts', img_file)


def _get_bar_rectangles(axis):
    for rect in axis.get_children():
        if not isinstance(rect, Rectangle):
            continue

        # Assume white rectangles are not bars
        if rect.get_facecolor() == (1, 1, 1, 1):
            continue
        yield rect


def horizontal_bar(data_frame, destination_file, color='#849F38', xlabel='',
                   ylabel='', **kwargs):
    data_frame.plot(kind='barh', color=color, linewidth=0)

    ax = plt.gca()

    # Turn off y-axis grid
    ax.yaxis.grid(False)

    # Set axis labels
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')

    _format_ticks(ax)

    # Add labels to rectangles
    for rect in _get_bar_rectangles(ax):
        width = rect.get_width()
        ax.text(width - (data_frame.max() * 0.05),
                rect.get_y() + rect.get_height() / 2. - .03,
                '%d' % int(width), ha='center', va='bottom', color='white',
                fontweight='bold')

    return _save_chart(destination_file, **kwargs)


def vertical_bar(data_frame, destination_file, color='#849F38', xlabel='',
                 ylabel='', **kwargs):
    data_frame.plot(kind='bar', color=color, linewidth=0)

    ax = plt.gca()

    # Turn off x-axis grid
    ax.xaxis.grid(False)

    # Set axis labels
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')

    _format_ticks(ax)

    # Add labels to rectangles
    for rect in _get_bar_rectangles(ax):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2.0,
                height - (data_frame.max() * 0.05),
                '%d' % int(height), ha='center', va='bottom', color='white',
                fontweight='bold')

    return _save_chart(destination_file, **kwargs)


def line_fill(data_frame, destination_file, color='#F63C04', xlabel='',
              ylabel='', **kwargs):
    data_frame.plot(kind='line', color=color, linewidth=1)

    ax = plt.gca()

    # Turn off x-axis grid
    ax.xaxis.grid(False)

    # Set axis labels
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')

    _format_ticks(ax)

    # Fill between the line and y=0
    ax.fill_between(sorted(data_frame.keys()), 0, data_frame.values, color=color)

    return _save_chart(destination_file, **kwargs)