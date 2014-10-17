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


def horizontal_bar(data_frame, destination_file, color='#849F38', xlabel='',
                   ylabel=''):
    data_frame.plot(kind='barh', color=color, linewidth=0)

    ax = plt.gca()

    # Turn off y-axis grid
    ax.yaxis.grid(False)

    # Set axis labels
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')

    # Remove top, right ticks
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Remove top, right ticks
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Make ticks face out
    ax.xaxis.set_tick_params(direction='out')
    ax.yaxis.set_tick_params(direction='out', labelsize=14)

    # Add labels to rectangles
    for rect in ax.get_children():
        if not isinstance(rect, Rectangle):
            continue
        if rect.get_facecolor() == (1, 1, 1, 1):
            continue
        width = rect.get_width()
        ax.text(width - (data_frame.max() * 0.05),
                rect.get_y() + rect.get_height() / 2. - .03,
                '%d' % int(width), ha='center', va='bottom', color='white',
                fontweight='bold')

    # Do our best to get an appropriate file name and make room for it
    img_file = destination_file
    if not img_file.endswith('.png'):
        img_file = '%s.png' % img_file
    filename = os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'charts', img_file))
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    # Save
    pylab.savefig(filename, bbox_inches='tight')

    # Close this plot so we don't affect other plots
    plt.clf()
    plt.cla()
    return os.path.join('charts', img_file)
