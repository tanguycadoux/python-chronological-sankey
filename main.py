import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import json
import os
from datetime import datetime, timedelta
import numpy as np


def get_dates_boundaries(diagram_data):
    min_date = diagram_data[0]['date-begin']
    max_date = diagram_data[0]['date-end']
    for item in diagram_data[1:]:
        min_date = min(min_date, item['date-begin'])
        max_date = max(max_date, item['date-end'])
    return (min_date, max_date)

def get_rows_boundaries(diagram_data):
    min_row = diagram_data[0]['row']
    max_row = diagram_data[0]['row']
    for item in diagram_data[1:]:
        min_row = min(min_row, item['row'])
        max_row = max(max_row, item['row'])
    return (min_row, max_row)

def load_json(filename):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, filename), 'r') as file:
        json_file = json.load(file)
    return json_file


TEXT_PADDING = 5
EDGESIZE = 2
ROW_HEIGHT_INCH = 3
ROW_PADDING = .5

diagram_data = load_json('test-file.json')['chronological_sankey_data']
(min_row, max_row) = get_rows_boundaries(diagram_data)
(min_date, max_date) = get_dates_boundaries(diagram_data)

with mpl.rc_context({
    'xtick.minor.size': 2,
    'xtick.major.size': 12}):

    fig, ax = plt.subplots(figsize=(12, (max_row - min_row)*ROW_HEIGHT_INCH))

    for i, item in enumerate(diagram_data):
        start = mdates.date2num(datetime.fromisoformat(item['date-begin']))
        end = mdates.date2num(datetime.fromisoformat(item['date-end']))
        ax.add_patch(plt.Rectangle((start, -item['row']), end-start, 1, lw=EDGESIZE, ec='k', label=item['group']))
        ax.text(start + TEXT_PADDING, -item['row']+.5, item['name'], verticalalignment='center_baseline', fontsize=15)

    ax.set_xlim([mdates.date2num(datetime.fromisoformat(min_date)),
                mdates.date2num(datetime.fromisoformat(max_date))])

    ax.set_ylim([-max_row-ROW_PADDING,
                1-min_row+ROW_PADDING])

    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.get_yaxis().set_visible(False)

    ax.spines.left.set_visible(False)
    ax.spines.right.set_visible(False)

    ax.grid(True)

    ax.legend()

    plt.show()
