import matplotlib.pyplot as plt
import json
import os
import matplotlib.dates as mdates
from datetime import datetime
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

def draw_rectangle(ax, x0, y0, width, height, edge_size):
    p = plt.Rectangle((x0, y0), width, height, ec='k', lw=edge_size)
    ax.add_patch(p)


TEXT_PADDING = 5
EDGESIZE = 2
ROW_HEIGHT_INCH = 2
FIG_DPI = 100 # pixels per inch
FIG_PPI = 50 # points per inch

edge_outer_size_inch = EDGESIZE/FIG_PPI
# Pas exactement ça...... 
edge_outer_size_data_units = (0, edge_outer_size_inch/ROW_HEIGHT_INCH)

diagram_data = load_json('test-file.json')
(min_row, max_row) = get_rows_boundaries(diagram_data)

fig, ax = plt.subplots(figsize=(8, (max_row - min_row)*ROW_HEIGHT_INCH), dpi=FIG_DPI)

for i, item in enumerate(diagram_data):
    start = mdates.date2num(datetime.fromisoformat(item['date-begin']))
    end = mdates.date2num(datetime.fromisoformat(item['date-end']))
    draw_rectangle(ax, start, -item['row'], end-start, 1, EDGESIZE)
    ax.text(start + TEXT_PADDING, -item['row']+.5, item['name'], verticalalignment='center_baseline', fontsize=15)

(min_date, max_date) = get_dates_boundaries(diagram_data)
ax.set_xlim([mdates.date2num(datetime.fromisoformat(min_date))-abs(edge_outer_size_data_units[0]),
             mdates.date2num(datetime.fromisoformat(max_date))+abs(edge_outer_size_data_units[0])])

ax.set_ylim([-max_row-abs(edge_outer_size_data_units[1]),
             1-min_row+abs(edge_outer_size_data_units[1])])

ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.get_yaxis().set_visible(False)

ax.spines.left.set_visible(False)
ax.spines.right.set_visible(False)

ax.grid(True)

plt.show()
